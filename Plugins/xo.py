'''


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/W_WT1"}
- XO Game (Tic-Tac-Toe)

'''
import random
import json
import time
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *

# ──────────────────────────────────────
# Store active XO games in memory
# Key: chat_id:msg_id -> game_data dict
# ──────────────────────────────────────
xo_games = {}

EMPTY = "⬜"
X_MARK = "❌"
O_MARK = "⭕"

WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6]              # diags
]


def make_board_markup(board, game_id, game_over=False):
    """Create inline keyboard markup for the XO board."""
    buttons = []
    for row_start in range(0, 9, 3):
        row = []
        for i in range(row_start, row_start + 3):
            cell = board[i]
            if cell == EMPTY and not game_over:
                row.append(InlineKeyboardButton(" ", callback_data=f"xo:{game_id}:{i}"))
            else:
                row.append(InlineKeyboardButton(cell, callback_data=f"xo_none"))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def check_winner(board):
    """Check if there's a winner. Returns X_MARK, O_MARK, 'draw', or None."""
    for combo in WIN_COMBOS:
        a, b, cc = combo
        if board[a] == board[b] == board[cc] and board[a] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def bot_move(board):
    """Simple AI for single player mode."""
    # 1. Try to win
    for combo in WIN_COMBOS:
        cells = [board[i] for i in combo]
        if cells.count(O_MARK) == 2 and cells.count(EMPTY) == 1:
            return combo[cells.index(EMPTY)]
    # 2. Block opponent
    for combo in WIN_COMBOS:
        cells = [board[i] for i in combo]
        if cells.count(X_MARK) == 2 and cells.count(EMPTY) == 1:
            return combo[cells.index(EMPTY)]
    # 3. Take center
    if board[4] == EMPTY:
        return 4
    # 4. Take corners
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for c in corners:
        if board[c] == EMPTY:
            return c
    # 5. Take any available
    available = [i for i in range(9) if board[i] == EMPTY]
    if available:
        return random.choice(available)
    return None


# ──────────────────────────────────────
# Message handler: start XO game
# ──────────────────────────────────────
@Client.on_message(filters.text & filters.group, group=77)
def xo_message_handler(c, m):
    if not getattr(m, 'from_user', None):
        return
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return
    if r.get(f'{m.chat.id}:disableGames:{Dev_Zaid}'):
        return

    k = r.get(f'{Dev_Zaid}:botkey')
    text = m.text.strip()

    # ── Two-player mode: reply to someone with "اكس او" ──
    if text in ['اكس او', 'xo', 'XO', 'Xo', 'اكسو', 'أكس أو']:
        if m.reply_to_message and m.reply_to_message.from_user:
            opponent = m.reply_to_message.from_user
            if opponent.id == m.from_user.id:
                return m.reply(f"{k} ماتقدر تلعب مع نفسك 😅")
            if opponent.is_bot:
                return m.reply(f"{k} ماتقدر تلعب مع بوت 🤖")

            board = [EMPTY] * 9
            game_id = f"{m.chat.id}_{int(time.time())}_{m.from_user.id}"

            player_x_name = m.from_user.first_name[:15]
            player_o_name = opponent.first_name[:15]

            game_data = {
                "board": board,
                "turn": "X",
                "player_x": m.from_user.id,
                "player_o": opponent.id,
                "player_x_name": player_x_name,
                "player_o_name": player_o_name,
                "chat_id": m.chat.id,
                "vs_bot": False,
                "game_id": game_id,
            }

            markup = make_board_markup(board, game_id)
            msg = m.reply(
                f"🎮 **لعبة اكس او**\n\n"
                f"❌ {m.from_user.mention} **ضد** ⭕ {opponent.mention}\n\n"
                f"📌 دور: {m.from_user.mention} ({X_MARK})",
                reply_markup=markup
            )
            game_data["msg_id"] = msg.id
            xo_games[game_id] = game_data
            # Auto-expire game after 5 minutes
            Thread(target=_expire_game, args=(game_id, 300), daemon=True).start()
            return

        # ── Single-player mode: just "اكس او" without reply ──
        else:
            board = [EMPTY] * 9
            game_id = f"{m.chat.id}_{int(time.time())}_{m.from_user.id}"
            bot_name = r.get(f'{Dev_Zaid}:BotName') or 'البوت'

            game_data = {
                "board": board,
                "turn": "X",
                "player_x": m.from_user.id,
                "player_o": "bot",
                "player_x_name": m.from_user.first_name[:15],
                "player_o_name": bot_name,
                "chat_id": m.chat.id,
                "vs_bot": True,
                "game_id": game_id,
            }

            markup = make_board_markup(board, game_id)
            msg = m.reply(
                f"🎮 **لعبة اكس او**\n\n"
                f"❌ {m.from_user.mention} **ضد** ⭕ {bot_name} 🤖\n\n"
                f"📌 دورك انت ({X_MARK}) - اختر مربع!",
                reply_markup=markup
            )
            game_data["msg_id"] = msg.id
            xo_games[game_id] = game_data
            Thread(target=_expire_game, args=(game_id, 300), daemon=True).start()
            return


def _expire_game(game_id, seconds):
    """Auto-delete game after timeout."""
    time.sleep(seconds)
    if game_id in xo_games:
        del xo_games[game_id]


# ──────────────────────────────────────
# Callback handler: XO moves
# ──────────────────────────────────────
@Client.on_callback_query(filters.regex(r'^xo:'))
def xo_callback_handler(c, m):
    if not getattr(m, 'from_user', None):
        return

    k = r.get(f'{Dev_Zaid}:botkey')
    data = m.data  # e.g. "xo:game_id:cell"
    parts = data.split(":")
    if len(parts) < 3:
        return m.answer("❌ خطأ", show_alert=False)

    game_id = parts[1]
    cell = int(parts[2])

    if game_id not in xo_games:
        return m.answer("⏰ انتهت اللعبة أو ما بدأت!", show_alert=True)

    game = xo_games[game_id]
    board = game["board"]
    turn = game["turn"]
    player_x = game["player_x"]
    player_o = game["player_o"]
    vs_bot = game["vs_bot"]

    # Determine who should play
    current_player = player_x if turn == "X" else player_o

    # Check if it's this user's turn
    if current_player == "bot":
        return m.answer("🤖 دور البوت، انتظر!", show_alert=False)

    if m.from_user.id != current_player:
        if m.from_user.id in (player_x, player_o if player_o != "bot" else -1):
            return m.answer("⏳ مو دورك، انتظر!", show_alert=False)
        else:
            return m.answer("❌ هذي مو لعبتك!", show_alert=True)

    # Check if cell is valid
    if board[cell] != EMPTY:
        return m.answer("❌ هالمربع محجوز!", show_alert=False)

    # Place the mark
    mark = X_MARK if turn == "X" else O_MARK
    board[cell] = mark

    # Check for winner
    winner = check_winner(board)

    if winner:
        _finish_game(c, m, game, winner)
        return

    # Switch turn
    game["turn"] = "O" if turn == "X" else "X"

    # If vs bot and now it's bot's turn
    if vs_bot and game["turn"] == "O":
        # Update board to show player's move first
        bot_name = game["player_o_name"]
        markup = make_board_markup(board, game_id)
        m.edit_message_text(
            f"🎮 **لعبة اكس او**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** ⭕ {bot_name} 🤖\n\n"
            f"🤖 دور {bot_name}...",
            reply_markup=markup,
            disable_web_page_preview=True
        )

        # Bot makes a move
        bot_cell = bot_move(board)
        if bot_cell is not None:
            board[bot_cell] = O_MARK

        # Check winner after bot move
        winner = check_winner(board)
        if winner:
            _finish_game(c, m, game, winner)
            return

        # Switch back to player
        game["turn"] = "X"
        markup = make_board_markup(board, game_id)
        m.edit_message_text(
            f"🎮 **لعبة اكس او**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** ⭕ {bot_name} 🤖\n\n"
            f"📌 دورك انت ({X_MARK}) - اختر مربع!",
            reply_markup=markup,
            disable_web_page_preview=True
        )
    else:
        # Two-player mode: switch turn
        next_player_id = player_o if game["turn"] == "O" else player_x
        next_mark = O_MARK if game["turn"] == "O" else X_MARK
        next_name = game["player_o_name"] if game["turn"] == "O" else game["player_x_name"]
        markup = make_board_markup(board, game_id)
        m.edit_message_text(
            f"🎮 **لعبة اكس او**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** "
            f"⭕ [{game['player_o_name']}](tg://user?id={player_o})\n\n"
            f"📌 دور: [{next_name}](tg://user?id={next_player_id}) ({next_mark})",
            reply_markup=markup,
            disable_web_page_preview=True
        )

    m.answer()


def _finish_game(c, m, game, winner):
    """Handle game over state."""
    game_id = game["game_id"]
    board = game["board"]
    player_x = game["player_x"]
    player_o = game["player_o"]
    vs_bot = game["vs_bot"]
    k = r.get(f'{Dev_Zaid}:botkey')
    channel = r.get(f'{Dev_Zaid}:BotChannel') or 'eeeCASH'

    markup = make_board_markup(board, game_id, game_over=True)

    if winner == "draw":
        text = (
            f"🎮 **لعبة اكس او - انتهت!**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** "
        )
        if vs_bot:
            text += f"⭕ {game['player_o_name']} 🤖\n\n"
        else:
            text += f"⭕ [{game['player_o_name']}](tg://user?id={player_o})\n\n"
        text += "🤝 **تعادل!** ماحد فاز"
    elif winner == X_MARK:
        text = (
            f"🎮 **لعبة اكس او - انتهت!**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** "
        )
        if vs_bot:
            text += f"⭕ {game['player_o_name']} 🤖\n\n"
        else:
            text += f"⭕ [{game['player_o_name']}](tg://user?id={player_o})\n\n"
        text += f"🏆 **الفائز:** [{game['player_x_name']}](tg://user?id={player_x}) ({X_MARK})"

        # Give winner money reward
        reward = random.randint(50, 200)
        if r.get(f'{player_x}:Floos'):
            floos = int(r.get(f'{player_x}:Floos'))
            r.set(f'{player_x}:Floos', floos + reward)
        else:
            r.set(f'{player_x}:Floos', reward)
        text += f"\n💸 +{reward} ريال مكافأة الفوز!"

    elif winner == O_MARK:
        text = (
            f"🎮 **لعبة اكس او - انتهت!**\n\n"
            f"❌ [{game['player_x_name']}](tg://user?id={player_x}) **ضد** "
        )
        if vs_bot:
            text += f"⭕ {game['player_o_name']} 🤖\n\n"
            text += f"🏆 **الفائز:** {game['player_o_name']} 🤖 ({O_MARK})"
            text += f"\n😢 للأسف خسرت!"
        else:
            text += f"⭕ [{game['player_o_name']}](tg://user?id={player_o})\n\n"
            text += f"🏆 **الفائز:** [{game['player_o_name']}](tg://user?id={player_o}) ({O_MARK})"
            # Give winner money reward
            reward = random.randint(50, 200)
            if r.get(f'{player_o}:Floos'):
                floos = int(r.get(f'{player_o}:Floos'))
                r.set(f'{player_o}:Floos', floos + reward)
            else:
                r.set(f'{player_o}:Floos', reward)
            text += f"\n💸 +{reward} ريال مكافأة الفوز!"

    # Add play again hint
    text += f"\n\n{k} للعب مرة ثانية اكتب: `اكس او`"

    m.edit_message_text(text, reply_markup=markup, disable_web_page_preview=True)

    # Clean up
    if game_id in xo_games:
        del xo_games[game_id]


@Client.on_callback_query(filters.regex(r'^xo_none$'))
def xo_none_callback(c, m):
    """Handle clicks on already-filled cells or game-over cells."""
    m.answer()
