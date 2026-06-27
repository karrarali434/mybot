"""


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/W_WT1"}


"""

import random, re, time, pytz, os, gtts, requests
import speech_recognition as sr
from pydub import AudioSegment
from hijri_converter import Hijri, Gregorian
from datetime import datetime
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.persianData import persianInformation
from .welcome_and_rules import *
from .games import *
from PIL import Image
from asyncio import run as RUN
from Python_ARQ import ARQ
from aiohttp import ClientSession

# from googletrans import Translator as googletranstr
from mutagen.mp3 import MP3 as mutagenMP3
# from main import TelegramBot

ARQ_API_KEY = "OZJRWV-SAURXD-PMBUKF-GMVSNS-ARQ"
ARQ_API_URL = "https://arq.hamker.dev"

# translator = googletranstr()

import json as _json

def _build_promote_keyboard(user_id, chat_id, perms):
    """Build inline keyboard for promote permissions toggle"""
    _icons = {
        "del": ("🗑", "حذف الرسائل"),
        "pin": ("📌", "تثبيت الرسائل"),
        "ban": ("🚫", "حظر الأعضاء"),
        "inv": ("🔗", "دعوة الأعضاء"),
        "vid": ("🎙", "المكالمات"),
        "info": ("ℹ️", "تعديل المعلومات"),
        "promo": ("👑", "رفع المشرفين"),
    }
    rows = []
    for key, (icon, label) in _icons.items():
        status = "✅" if perms.get(key) else "❌"
        rows.append([InlineKeyboardButton(
            f"{status} {icon} {label}",
            callback_data=f"prm_{key}_{user_id}_{chat_id}"
        )])
    rows.append([
        InlineKeyboardButton("✅ تم", callback_data=f"prm_done_{user_id}_{chat_id}"),
        InlineKeyboardButton("❌ إلغاء", callback_data=f"prm_cancel_{user_id}_{chat_id}"),
    ])
    rows.append([
        InlineKeyboardButton("تحديد الكل ☑️", callback_data=f"prm_all_{user_id}_{chat_id}"),
        InlineKeyboardButton("إلغاء الكل ✖️", callback_data=f"prm_none_{user_id}_{chat_id}"),
    ])
    return InlineKeyboardMarkup(rows)


def _print_report(c, m, target_id, mention, k):
    """Generate and send a print report for a user's restrictions."""
    report = f"📋 برنت العضو: {mention}\n"
    report += f"🆔 الايدي: `{target_id}`\n"
    report += "━━━━━━━━━━━━━━━\n\n"

    # Check status from Telegram
    is_banned = False
    is_restricted = False
    try:
        member = m.chat.get_member(target_id)
        is_banned = member.status == ChatMemberStatus.BANNED
        is_restricted = member.status == ChatMemberStatus.RESTRICTED
    except:
        pass

    # Check bot's Redis data
    is_muted = bool(r.get(f'{target_id}:mute:{m.chat.id}{Dev_Zaid}'))
    is_gmuted = bool(r.get(f'{target_id}:mute:{Dev_Zaid}'))
    is_gbanned = bool(r.get(f'{target_id}:gban:{Dev_Zaid}'))
    is_gbanned_games = bool(r.get(f'{target_id}:gbangames:{Dev_Zaid}'))

    has_any = is_banned or is_restricted or is_muted or is_gmuted or is_gbanned or is_gbanned_games

    # 1. Ban section
    report += f"🔴 الحظر: {'✅ محظور' if is_banned else '❌ غير محظور'}\n"
    ban_data = r.get(f'{m.chat.id}:print:ban:{target_id}{Dev_Zaid}')
    if ban_data:
        try:
            bd = _json.loads(ban_data)
            report += f"├ من قام بالحظر: [{bd.get('name', '؟')}](tg://user?id={bd.get('id', 0)})\n"
            report += f"└ السبب: {bd.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 2. Restrict section
    report += f"🟡 التقييد: {'✅ مقيد' if is_restricted else '❌ غير مقيد'}\n"
    restrict_data = r.get(f'{m.chat.id}:print:restrict:{target_id}{Dev_Zaid}')
    if restrict_data:
        try:
            rd = _json.loads(restrict_data)
            report += f"├ من قام بالتقييد: [{rd.get('name', '؟')}](tg://user?id={rd.get('id', 0)})\n"
            report += f"└ السبب: {rd.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 3. Mute section
    report += f"🔵 الكتم: {'✅ مكتوم' if is_muted else '❌ غير مكتوم'}\n"
    mute_data = r.get(f'{m.chat.id}:print:mute:{target_id}{Dev_Zaid}')
    if mute_data:
        try:
            md = _json.loads(mute_data)
            report += f"├ من قام بالكتم: [{md.get('name', '؟')}](tg://user?id={md.get('id', 0)})\n"
            report += f"└ السبب: {md.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 4. Global ban
    report += f"🟣 الحظر العام: {'✅ محظور عام' if is_gbanned else '❌ غير محظور عام'}\n"
    gban_data = r.get(f'print:gban:{target_id}{Dev_Zaid}')
    if gban_data:
        try:
            gd = _json.loads(gban_data)
            report += f"├ من قام بالحظر: [{gd.get('name', '؟')}](tg://user?id={gd.get('id', 0)})\n"
            report += f"└ السبب: {gd.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 5. Global mute
    report += f"🟤 الكتم العام: {'✅ مكتوم عام' if is_gmuted else '❌ غير مكتوم عام'}\n"
    gmute_data = r.get(f'print:gmute:{target_id}{Dev_Zaid}')
    if gmute_data:
        try:
            gmd = _json.loads(gmute_data)
            report += f"├ من قام بالكتم: [{gmd.get('name', '؟')}](tg://user?id={gmd.get('id', 0)})\n"
            report += f"└ السبب: {gmd.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 6. Games global ban
    report += f"🟠 حظر الالعاب: {'✅ محظور' if is_gbanned_games else '❌ غير محظور'}\n"
    gbgames_data = r.get(f'print:gbangames:{target_id}{Dev_Zaid}')
    if gbgames_data:
        try:
            ggd = _json.loads(gbgames_data)
            report += f"├ من قام بالحظر: [{ggd.get('name', '؟')}](tg://user?id={ggd.get('id', 0)})\n"
            report += f"└ السبب: {ggd.get('reason', 'لا يوجد')}\n"
        except:
            pass
    report += "\n"

    # 7. Kick history
    kick_data = r.get(f'{m.chat.id}:print:kick:{target_id}{Dev_Zaid}')
    if kick_data:
        try:
            kd = _json.loads(kick_data)
            report += f"⚪ الطرد: ✅ تم طردة مسبقاً\n"
            report += f"├ من قام بالطرد: [{kd.get('name', '؟')}](tg://user?id={kd.get('id', 0)})\n"
            report += f"└ السبب: {kd.get('reason', 'لا يوجد')}\n"
            has_any = True
        except:
            pass

    report += "\n━━━━━━━━━━━━━━━\n"
    if not has_any:
        report += f"{k} العضو ماعليه اي قيود ☆"
    else:
        report += "☆"
    return m.reply(report, disable_web_page_preview=True)


list_UwU = [
    "كس",
    "كسمك",
    "كسختك",
    "عير",
    "كسخالتك",
    "خرا بالله",
    "عير بالله",
    "كسخواتكم",
    "كحاب",
    "مناويج",
    "مناويج",
    "كحبه",
    "ابن الكحبه",
    "فرخ",
    "فروخ",
    "طيزك",
    "طيزختك",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "ابن العرص",
    "منايك",
    "متناك",
    "ابن المتناكه",
    "زبك",
    "عرص",
    "زبي",
    "خول",
    "لبوه",
    "لباوي",
    "ابن اللبوه",
    "منيوك",
    "كسمكك",
    "متناكه",
    "يا عرص",
    "يا خول",
    "قحبه",
    "القحبه",
    "شراميط",
    "العلق",
    "العلوق",
    "العلقه",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "االمنيوك",
    "كسمككك",
    "الشرموطه",
    "ابن العرث",
    "ابن الحيضانه",
    "زبك",
    "خول",
    "زبي",
    "قاحب",
]

list_Shiaa = [
    "يا علي",
    "يا حسين",
    "ياعلي",
    "ياحسين",
    "علي ولي الله",
    "عليا ولي الله",
    "عائشه زانيه",
    "عائشة زانية",
    "عائشة عاهرة",
    "عائشه عاهره",
    "خرب ربك",
    "خرب الله",
    "يلعن ربك",
    "يلعن الله",
    "يا عمر",
    "ياعمر",
    "يا محمد",
    "يامحمد",
    "زوجات الرسول",
    "عير بالسنة",
    "عير بالسنه",
    "خرب السنه",
    "خرا بالسنه",
    "خرب السنة",
    "خرا بالسنة",
    "والحسين",
    "والعباس",
    "وعلي",
    "والامام علي",
    "ربنا علي",
    "علي الله",
    "الله علي",
    "رب علي",
    "علي رب",
]


def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return [x[0] for x in url]


"""
         r.get(f'{m.chat.id}:mute:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockJoin:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockChannels:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockEdit:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockEditM:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockVoice:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockVideo:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockNot:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockPhoto:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockStickers:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockAnimations:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockFiles:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockPersian:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockUrls:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockHashtags:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockMessages:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockTags:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockBots:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockSpam:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockInline:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockForward:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockAudios:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockaddContacts:{Dev_Zaid}')
         r.get(f'{m.chat.id}:lockSHTM:{Dev_Zaid}')
"""

from pyrogram.errors import UserNotParticipant, FloodWait


@Client.on_message(filters.group, group=-1111111111111)
async def on_zbi(c: Client, m: Message):
    if not getattr(m, 'from_user', None): return
    if not getattr(m, "from_user", None): return
    name = r.get(f"{Dev_Zaid}:BotName") if r.get(f"{Dev_Zaid}:BotName") else "اتاك"
    text = m.text
    if text:
        if text.startswith(f"{name} "):
            text = text.replace(f"{name} ", "")
        if r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}"):
            text = r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}")
        if r.get(f"Custom:{Dev_Zaid}&text={text}"):
            text = r.get(f"Custom:{Dev_Zaid}&text={text}")

    if r.get(f"inDontCheck:{Dev_Zaid}"):
        return m.continue_propagation()

    if dev_pls(m.from_user.id, m.chat.id):
        return m.continue_propagation()

    if text and (
        text.startswith("تفعيل ")
        or text.startswith("تعطيل ")
        or text.startswith("قفل ")
        or text.startswith("فتح ")
        or text == "ايدي"
        or text == "الاوامر"
    ):
        if r.get(f"forceChannel:{Dev_Zaid}") and (
            not r.get(f"disableSubscribe:{Dev_Zaid}")
        ):
            username = r.get(f"forceChannel:{Dev_Zaid}").replace("@", "")
            if r.get(f"isMember:{m.from_user.id}:{username}"):
                return m.continue_propagation()
            not_member = False
            try:
                member = await c.get_chat_member(username, m.from_user.id)
            except FloodWait:
                return m.continue_propagation()
            except UserNotParticipant:
                await m.reply(
                    f"- انضم للقناة ( @{username} ) لتستطيع استخدام اوامر البوت",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "اضغط هنا", url="https://t.me/" + username
                                )
                            ]
                        ]
                    ),
                )
                r.set(f"inDontCheck:{Dev_Zaid}", 1, ex=10)
                return m.stop_propagation()
            except Exception as e:
                print(e)
                return m.continue_propagation()

            if member.status in {
                enums.ChatMemberStatus.LEFT,
                enums.ChatMemberStatus.BANNED,
            } or member.status is None:
                not_member = True
            else:
                not_member = False

            if not_member:
                await m.reply(
                    f"- انضم للقناة ( @{username} ) لتستطيع استخدام اوامر البوت",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "اضغط هنا", url="https://t.me/" + username
                                )
                            ]
                        ]
                    ),
                )
                r.set(f"inDontCheck:{Dev_Zaid}", 1, ex=10)
                return m.stop_propagation()
            else:
                r.set(f"isMember:{m.from_user.id}:{username}", 1, ex=3600)
                return m.continue_propagation()


@Client.on_message(filters.group, group=27)
def guardLocksResponse(c, m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f"{Dev_Zaid}:botkey")
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "eeeCASH"
    )
    Thread(target=guardResponseFunction, args=(c, m, k, channel)).start()


@Client.on_edited_message(filters.group, group=27)
def guardLocksResponse2(c, m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f"{Dev_Zaid}:botkey")
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "eeeCASH"
    )
    Thread(target=guardResponseFunction2, args=(c, m, k, channel)).start()


def guardResponseFunction2(c, m, k, channel):
    if not getattr(m, 'from_user', None): return
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return
    warner = """
「 {} 」
{} ممنوع {}
☆
"""
    warn = False
    reason = False

    if m.sender_chat:
        id = m.sender_chat.id
        mention = f"[{m.sender_chat.title}](t.me/{channel})"
    if m.from_user:
        id = m.from_user.id
        mention = m.from_user.mention

    if (
        r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}")
        and m.text
        and not pre_pls(id, m.chat.id)
    ):
        m.delete()
        warn = True
        reason = "التعديل"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if (
        r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
        and m.media
        and not pre_pls(id, m.chat.id)
    ):
        m.delete()
        warn = True
        reason = "تعديل الميديا"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )


def guardResponseFunction(c, m, k, channel):
    if not getattr(m, 'from_user', None): return
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return
    warner = """
「 {} 」
{} ممنوع {}
☆
"""
    warn = False
    reason = False

    if r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}") and m.service:
        m.delete()

    if (
        r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}")
        and m.from_user
        and m.new_chat_members
    ):
        if pre_pls(m.from_user.id, m.chat.id):
            return
        for me in m.new_chat_members:
            if not me.id == m.from_user.id:
                warn = True
                mention = m.from_user.mention
                m.chat.ban_member(me.id)
                reason = "تضيف حد هنا"
                m.delete()
                if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                    return m.reply(
                        warner.format(mention, k, reason), disable_web_page_preview=True
                    )

    if m.sender_chat:
        id = m.sender_chat.id
        mention = f"[{m.sender_chat.title}](t.me/{channel})"
    if m.from_user:
        id = m.from_user.id
        mention = m.from_user.mention

    # print(id)


    if r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
        if not mod_pls(id, m.chat.id):
            if m.photo or m.voice or m.animation or m.sticker or m.video:
                try:
                    m.delete()
                except:
                    pass
                return m.reply(f"「 {mention} 」\n{k} ممنوع إرسال الميديا بسبب الوضع الليلي\n☆", disable_web_page_preview=True)

    if m.media:
        rep = m
        if rep.sticker:
            file_id = rep.sticker.file_id
        if rep.animation:
            file_id = rep.animation.file_id
        if rep.photo:
            file_id = rep.photo.file_id
        if rep.video:
            file_id = rep.video.file_id
        if rep.voice:
            file_id = rep.voice.file_id
        if rep.audio:
            file_id = rep.audio.file_id
        if rep.document:
            file_id = rep.document.file_id
        idd = file_id[-6:]
        if r.get(f"{idd}:NotAllow:{m.chat.id}{Dev_Zaid}"):
            if not admin_pls(id, m.chat.id):
                return m.delete()

    if m.text and r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"):
        if not admin_pls(id, m.chat.id):
            for word in r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                if word in m.text:
                    return m.delete()

    if r.get(f"{id}:mute:{m.chat.id}{Dev_Zaid}") or r.get(f"{id}:mute:{Dev_Zaid}"):
        return False

    if r.get(f"{m.chat.id}:mute:{Dev_Zaid}") and not admin_pls(id, m.chat.id):
        m.delete()
        return False

    if pre_pls(id, m.chat.id):
        return False

    if r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}") and m.new_chat_members:
        for mem in m.new_chat_members:
            if mem.is_bot:
                return m.chat.ban_member(mem.id)

    if r.get(f"{m.chat.id}:lockBotsKick:{Dev_Zaid}") and m.new_chat_members:
        for mem in m.new_chat_members:
            if mem.is_bot:
                if not admin_pls(mem.id, m.chat.id):
                    m.chat.ban_member(mem.id)
                    m.chat.unban_member(mem.id)
                    return False

    if r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}") and m.new_chat_members:
        for mem in m.new_chat_members:
            if not admin_pls(mem.id, m.chat.id):
                m.chat.ban_member(mem.id)
                m.chat.unban_member(mem.id)
                return False

    if r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}") and m.sender_chat:
        if not m.sender_chat.id == m.chat.id:
            m.chat.ban_member(m.sender_chat.id)
            return False

    if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
        limit = int(r.get(f"{m.chat.id}:spamLimit:{Dev_Zaid}") or 10)
        if not r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"):
            r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", 1, ex=10)
        else:
            if int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")) >= limit:
                if m.from_user:
                    r.set(f"{id}:mute:{m.chat.id}{Dev_Zaid}", 1)
                    r.sadd(f"{m.chat.id}:listMUTE:{Dev_Zaid}", id)
                    r.delete(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")
                    return m.reply(
                        f"「 {mention} 」 \n{k} كتمتك يالبثر عشان تتعلم تكرر\n☆"
                    )

                if m.sender_chat:
                    m.chat.ban_member(m.sender_chat.id)
                    return m.reply(
                        f"「 {mention} 」 {k} حظرتك يالبثر عشان تتعلم تكرر\n☆"
                    )
            else:
                get = int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"))
                r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", get + 1, ex=10)

    if r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}") and m.via_bot:
        m.delete()
        warn = True
        reason = "ترسل انلاين"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}") and m.forward_date:
        m.delete()
        warn = True
        reason = "ترسل توجيه"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    """
  if r.get(f'{m.chat.id}:lockForward:{Dev_Zaid}') and m.forward_from_chat:
     m.delete()
     warn = True
     reason = 'ترسل توجيه'
     if not r.get(f'{m.chat.id}:disableWarn:{Dev_Zaid}') and not r.get(f'{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}'):
        r.set(f'{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}',1,ex=60)
        return m.reply(warner.format(mention,k,reason),disable_web_page_preview=True)
  """

    if r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}") and m.audio:
        m.delete()
        warn = True
        reason = "ترسل صوت"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}") and m.video:
        m.delete()
        warn = True
        reason = "ترسل فيديوهات"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}") and m.photo:
        m.delete()
        warn = True
        reason = "ترسل صور"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}") and m.sticker:
        m.delete()
        warn = True
        reason = "ترسل ملصقات"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}") and m.animation:
        m.delete()
        warn = True
        reason = "ترسل متحركات"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}") and m.document:
        m.delete()
        warn = True
        reason = "ترسل ملفات"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}") and m.text:
        if "ه‍" in m.text or "ی" in m.text or "ک" in m.text or "چ" in m.text:
            m.delete()
            warn = True
            reason = "ترسل فارسي"
            if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                return m.reply(
                    warner.format(mention, k, reason), disable_web_page_preview=True
                )

    if r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}") and m.caption:
        if "ه‍" in m.caption or "ی" in m.caption or "ک" in m.caption or "چ" in m.caption:
            m.delete()
            warn = True
            reason = "ترسل فارسي"
            if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                return m.reply(
                    warner.format(mention, k, reason), disable_web_page_preview=True
                )

    if (
        r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
        and m.text
        and len(Find(m.text.html)) > 0
    ):
        m.delete()
        warn = True
        reason = "ترسل روابط"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if (
        r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}")
        and m.text
        and len(re.findall(r"#(\w+)", m.text)) > 0
    ):
        m.delete()
        warn = True
        reason = "ترسل هاشتاق"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}") and m.text and len(m.text) > 150:
        m.delete()
        warn = True
        reason = "ترسل كلام كثير"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}") and m.voice:
        m.delete()
        warn = True
        reason = "ترسل فويس"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(
        f"{m.chat.id}:lockTags:{Dev_Zaid}"
    ) and '"type": "MessageEntityType.MENTION"' in str(m):
        m.delete()
        warn = True
        reason = "ترسل منشنات"
        if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
            return m.reply(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}") and (m.caption or m.text):
        if m.caption:
            txt = m.caption
        if m.text:
            txt = m.text
        for a in list_UwU:
            if txt == a or f" {a} " in txt or a in txt:
                m.delete()
                warn = True
                reason = "السب هنا"
                if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
                    f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}"
                ):
                    r.set(f"{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}", 1, ex=60)
                    return m.reply(
                        warner.format(mention, k, reason), disable_web_page_preview=True
                    )

    """
  if r.get(f'{m.chat.id}:lockKFR:{Dev_Zaid}') and (m.caption or m.text):
     if m.caption:
         txt = m.caption.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","").replace("ـ","").replace("َ","").replace("ٕ","").replace("ُ","").replace("ِ","").replace("ٰ","").replace("ٖ","").replace("ً","").replace("ّ","").replace("ٌ","").replace("ٍ","").replace("ْ","").replace("ٔ","").replace("'","").replace('"',"")
     if m.text:
         txt = m.text.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","").replace("ـ","").replace("َ","").replace("ٕ","").replace("ُ","").replace("ِ","").replace("ٰ","").replace("ٖ","").replace("ً","").replace("ّ","").replace("ٌ","").replace("ٍ","").replace("ْ","").replace("ٔ","").replace("'","").replace('"',"")
     for kfr in list_Shiaa:
         if kfr in txt:
            m.delete()
            warn = True
            reason = 'الكفر هنا'
            if not r.get(f'{m.chat.id}:disableWarn:{Dev_Zaid}') and not r.get(f'{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}'):
                 r.set(f'{Dev_Zaid}:inWARN:{m.from_user.id}{m.chat.id}',1,ex=60)
                 return m.reply(warner.format(mention,k,reason),disable_web_page_preview=True)
  """

    if r.get(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}") and m.new_chat_members:
        if m.from_user.first_name:
            if (
                m.from_user.first_name in persianInformation["names"]
                or m.from_user.id in persianInformation["ids"]
                or "ه‍" in m.from_user.first_name
                or "ی" in m.from_user.first_name
                or "ک" in m.from_user.first_name
                or "چ" in m.from_user.first_name
                or "👙" in m.from_user.first_name
            ) and not pre_pls(m.from_user.id, m.chat.id):
                if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                    m.reply(
                        """
「 {} 」
{} تم حظره لاشتباهه ببوت إيراني
☆
""".format(m.from_user.mention, k)
                    )
                return c.ban_chat_member(m.chat.id, m.from_user.id)

        if m.from_user.last_name:
            if (
                m.from_user.last_name in persianInformation["last_names"]
                or m.from_user.id in persianInformation["ids"]
                or "ه‍" in m.from_user.last_name
                or "ی" in m.from_user.last_name
                or "ک" in m.from_user.last_name
                or "چ" in m.from_user.last_name
                or "👙" in m.from_user.last_name
            ) and not pre_pls(m.from_user.id, m.chat.id):
                if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                    m.reply(
                        """
「 {} 」
{} تم حظره لاشتباهه ببوت إيراني
☆
""".format(m.from_user.mention, k)
                    )
                return c.ban_chat_member(m.chat.id, m.from_user.id)

    if r.get(f"{m.chat.id}:enableVerify:{Dev_Zaid}") and m.new_chat_members:
        for me in m.new_chat_members:
            if not pre_pls(me.id, m.chat.id):
                c.restrict_chat_member(
                    m.chat.id, me.id, ChatPermissions(can_send_messages=False)
                )
                get_random = get_for_verify(me)
                question = get_random["question"]
                reply_markup = get_random["key"]
                return m.reply(
                    f"{k} قيدناك عشان نتاكد انك شخص حقيقي مو زومبي\n\n{question}",
                    reply_markup=reply_markup,
                )

    if m.media and r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}"):
        print("nsfw scanner")
        if not admin_pls(id, m.chat.id):
            if m.sticker:
                id = m.sticker.thumbs[0].file_id
            if m.photo:
                id = m.photo.file_id
            if m.video:
                id = m.video.thumbs[0].file_id
            if m.animation:
                id = m.animation.thumbs[0].file_id
        file = c.download_media(id)
        Thread(target=scanR, args=(c, m, id, file)).start()


def scanR(c, m, id, file):
    if not getattr(m, 'from_user', None): return
    RUN(scan4(c, m, id, file))


async def scan4(c, m, id, file):
    if not getattr(m, 'from_user', None): return
    session = ClientSession()
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)
    resp = await arq.nsfw_scan(file=file)
    if resp.result.is_nsfw:
        print("xNSFW")
        await m.delete()
        k = r.get(f"{Dev_Zaid}:botkey")
        await m.reply(
            f"「 {m.from_user.mention} 」\n{k} تم حذف رسالتك لإحتوائها على محتوى إباحي .\n☆"
        )
    os.remove(file)
    await session.close()


def get_for_verify(me):
    for_verify = [
        {
            "question": "ماهو الحيوان الذي ينتهي اسمه بحرف الباء ؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("فأر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("وشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("بشار الأسد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("حمار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("كلب", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("قطة", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة فرنسا؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("باريس", callback_data=f"yes:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الكويت", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("القاهرة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماشا والدب", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "نادي يبدأ بحرف الباء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("برشلونا", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الهلال", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("النصر", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الزمالك", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ريال مدريد", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مانشستر", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "دولة يبدأ اسمها بحرف التاء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("قطر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("امريكا", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("سوريا", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("مصر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الصين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("تركيا", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🤑 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍭", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🤑", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌀", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🪨", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🔓 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("💸", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💣", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🔓", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🌠 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("☄️", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🦄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌠", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🌈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🧑‍💻", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة سوريا",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("دير الزور", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ادلب", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("ليو ميسي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مزة فيلات", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عملة الولايات المتحدة الأمريكية",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("الروبية", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الجنيه", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الليرة", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الدولار", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الدينار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الين", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مذكر يبدأ بحرف ز",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("زيد", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("علي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("محمد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("عمر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("المريخ", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("احمد", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث ينتهي بحرف ي",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أماني", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("أمل", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث يبدأ بحرف أ",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أمل", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("يمنى", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "الأسبوع كم يوم؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("2", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("3", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("4", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("5", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("6", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("7", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("8", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("9", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
    ]
    return random.choice(for_verify)


@Client.on_chat_join_request(filters.group, group=100)
def antiPersian(c, m):
    if not getattr(m, 'from_user', None): return
    if r.get(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}"):
        k = r.get(f"{Dev_Zaid}:botkey")
        if not pre_pls(m.from_user.id, m.chat.id):
            if m.from_user.first_name:
                if (
                    m.from_user.first_name in persianInformation["names"]
                    or m.from_user.id in persianInformation["ids"]
                    or "ه‍" in m.from_user.first_name
                    or "ی" in m.from_user.first_name
                    or "ک" in m.from_user.first_name
                    or "چ" in m.from_user.first_name
                    or "👙" in m.from_user.first_name
                ):
                    c.decline_chat_join_request(m.chat.id, m.from_user.id)
                    if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                        c.send_message(
                            m.chat.id,
                            """
「 {} 」
{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني
☆
""".format(m.from_user.mention, k),
                        )
                    return True
            if m.from_user.last_name:
                if (
                    m.from_user.last_name in persianInformation["last_names"]
                    or m.from_user.id in persianInformation["ids"]
                    or "ه‍" in m.from_user.last_name
                    or "ی" in m.from_user.last_name
                    or "ک" in m.from_user.last_name
                    or "چ" in m.from_user.last_name
                    or "👙" in m.from_user.last_name
                ):
                    c.decline_chat_join_request(m.chat.id, m.from_user.id)
                    if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                        c.send_message(
                            m.chat.id,
                            """
「 {} 」
{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني
☆
""".format(m.from_user.mention, k),
                        )
                    return True


@Client.on_message(filters.group & filters.text, group=28)
def guardCommandsHandler(c, m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f"{Dev_Zaid}:botkey")
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "eeeCASH"
    )
    Thread(target=guardCommands, args=(c, m, k, channel)).start()


def guardCommands(c, m, k, channel):
    if not getattr(m, 'from_user', None): return
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return False
    if r.get(f"{m.chat.id}:mute:{Dev_Zaid}") and not admin_pls(
        m.from_user.id, m.chat.id
    ):
        return False
    if r.get(f"{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}"):
        return False
    if r.get(f"{m.from_user.id}:mute:{Dev_Zaid}"):
        return False
    if r.get(f"{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}"):
        return False
    if r.get(f"{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}"):
        return False
    if r.get(f"{m.chat.id}:delCustom:{m.from_user.id}{Dev_Zaid}") or r.get(
        f"{m.chat.id}:delCustomG:{m.from_user.id}{Dev_Zaid}"
    ):
        return False
    text = m.text
    name = r.get(f"{Dev_Zaid}:BotName") if r.get(f"{Dev_Zaid}:BotName") else "اتاك"
    if text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "")
    if r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}"):
        text = r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}")
    if r.get(f"Custom:{Dev_Zaid}&text={text}"):
        text = r.get(f"Custom:{Dev_Zaid}&text={text}")
    if isLockCommand(m.from_user.id, m.chat.id, text):
        return
    Open = """
{} من 「 {} 」
{} ابشر فتحت {}
☆
"""
    Openn = """
{} من 「 {} 」
{} {} مفتوح من قبل
☆
"""
    Openn2 = """
{} من 「 {} 」
{} {} مفتوحه من قبل
☆
"""

    lock = """
{} من 「 {} 」
{} ابشر قفلت {}
☆
"""

    lockn = """
{} من 「 {} 」
{} {} مقفل من قبل
☆
"""
    locknn = """
{} من 「 {} 」
{} {} مقفله من قبل
☆
"""

    if text == "الاعدادات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            x1 = "مقفول" if r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}") else "مفتوح"
            x2 = "مقفول" if r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}") else "مفتوح"
            x3 = "مقفول" if r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}") else "مفتوح"
            x4 = "مقفول" if r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}") else "مفتوح"
            x5 = "مقفول" if r.get(f"{m.chat.id}:mute:{Dev_Zaid}") else "مفتوح"
            x6 = "مقفول" if r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}") else "مفتوح"
            x7 = "مقفول" if r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}") else "مفتوح"
            x8 = "مقفول" if r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}") else "مفتوح"
            x9 = "مقفول" if r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}") else "مفتوح"
            x10 = "مقفول" if r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}") else "مفتوح"
            x11 = "مقفول" if r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}") else "مفتوح"
            x12 = (
                "مقفول" if r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}") else "مفتوح"
            )
            x13 = "مقفول" if r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}") else "مفتوح"
            x14 = "مقفول" if r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}") else "مفتوح"
            x15 = "مقفول" if r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}") else "مفتوح"
            x16 = "مقفول" if r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}") else "مفتوح"
            x17 = (
                "مقفول" if r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}") else "مفتوح"
            )
            x18 = "مقفول" if r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}") else "مفتوح"
            x19 = "مقفول" if r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}") else "مفتوح"
            x20 = "مقفول" if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}") else "مفتوح"
            x21 = "مقفول" if r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}") else "مفتوح"
            x22 = "مقفول" if r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}") else "مفتوح"
            x23 = "مقفول" if r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}") else "مفتوح"
            x24 = "مقفول" if r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}") else "مفتوح"
            x25 = (
                "مقفول" if r.get(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}") else "مفتوح"
            )
            x26 = "مقفول" if r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}") else "مفتوح"
            return m.reply(f"""
اعدادات المجموعة :

{k} الملفات الصوتية ⇠ ( {x1} )
{k} الفيديو ⇠ ( {x2} )
{k} الفويس ⇠ ( {x3} )
{k} الصور ⇠ ( {x4} )

{k} الدردشة ⇠ ( {x5} )
{k} الانلاين ⇠ ( {x6} )
{k} التوجيه ⇠ ( {x7} )
{k} الهشتاق ⇠ ( {x8} )
{k} التعديل ⇠ ( {x9} )
{k} الستيكرات ⇠ ( {x10} )

{k} الملفات ⇠ ( {x11} )
{k} المتحركات ⇠ ( {x12} )
{k} الروابط ⇠ ( {x13} )
{k} البوتات ⇠ ( {x14} )
{k} اليوزرات ⇠ ( {x15} )

{k} الاشعارات ⇠ ( {x16} )
{k} الاضافة ⇠ ( {x17} )

{k} الكلام الكثير ⇠ ( {x18} )
{k} السب ⇠ ( {x19} )
{k} التكرار ⇠ ( {x20} )
{k} القنوات ⇠ ( {x21} )
{k} تعديل الميديا ⇠ ( {x22} )

{k} الدخول ⇠ ( {x23} )
{k} الفارسية ⇠ ( {x24} )
{k} دخول الإيراني ⇠ ( {x25} )
{k} الإباحي ⇠ ( {x26} )

~ @{channel}""")

    if text == "الساعه" or text == "الساعة" or text == "الوقت":
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        return m.reply(f"{k} الساعة ( {clock} )")

    if text == "القوانين":
        if r.get(f"{m.chat.id}:CustomRules:{Dev_Zaid}"):
            rules = r.get(f"{m.chat.id}:CustomRules:{Dev_Zaid}")
        else:
            rules = f"""{k} ممنوع نشر الروابط
{k} ممنوع التكلم او نشر صور اباحيه
{k} ممنوع اعاده توجيه
{k} ممنوع العنصرية بكل انواعها
{k} الرجاء احترام المدراء والادمنيه"""
        return m.reply(rules, disable_web_page_preview=True)

    if text == "التاريخ":
        b = Hijri.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        hijri = Hijri(year, month, day)
        hijri_date = str(b).replace("-", "/")
        hijri_month = hijri.month_name("ar")

        b = Gregorian.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        geo = Gregorian(year, month, day)
        geo_date = str(b).replace("-", "/")
        geo_month = geo.month_name("en")[:3]

        return m.reply(f"""
التاريخ:
{k} هجري ↢ {hijri_date} {hijri_month}
{k} ميلادي ↢ {geo_date} {geo_month}
""")

    if text.startswith("تغيير كليشة المالك "):
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        new_caption = text.replace("تغيير كليشة المالك ", "")
        r.set(f"{m.chat.id}:OwnerCaption:{Dev_Zaid}", new_caption)
        return m.reply(f"{k} تم حفظ كليشة المالك بنجاح.\\n\\nيمكنك استخدام المتغيرات:\\n`{{mention}}` - لمنشن المالك\\n`{{username}}` - لمعرف المالك\\n`{{id}}` - لايدي المالك")

    if text == "مسح كليشة المالك":
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        r.delete(f"{m.chat.id}:OwnerCaption:{Dev_Zaid}")
        return m.reply(f"{k} تم مسح كليشة المالك والعودة للافتراضية.")

    if text == "تغيير المالك" and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        new_owner_id = m.reply_to_message.from_user.id
        r.set(f"{m.chat.id}:CustomOwner:{Dev_Zaid}", new_owner_id)
        return m.reply(f"{k} تم تعيين {m.reply_to_message.from_user.mention} كمالك للمجموعة في البوت.")

    if text == "مسح المالك":
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        r.delete(f"{m.chat.id}:CustomOwner:{Dev_Zaid}")
        return m.reply(f"{k} تم مسح المالك المخصص والعودة لمالك المجموعة الحقيقي.")

    if text == "المالك":
        owner = None
        custom_owner_id = r.get(f"{m.chat.id}:CustomOwner:{Dev_Zaid}")
        
        if custom_owner_id:
            try:
                owner = c.get_users(int(custom_owner_id))
            except:
                pass

        if not owner:
            for mm in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
                if mm.status == ChatMemberStatus.OWNER:
                    owner = mm.user
                    break
                    
        if owner:
            if getattr(owner, 'is_deleted', False):
                m.reply("حساب المالك محذوف")
            else:
                owner_username = owner.username if owner.username else owner.id
                
                custom_caption = r.get(f"{m.chat.id}:OwnerCaption:{Dev_Zaid}")
                if custom_caption:
                    caption = custom_caption.replace("{mention}", owner.mention).replace("{username}", str(owner_username)).replace("{id}", str(owner.id))
                else:
                    caption = f"• Owner ☆ ↦ {owner.mention}\\n\\n"
                    caption += f"• Owner User ↦ @{owner_username}"
                    
                if owner.photo:
                    try:
                        file_id = owner.photo.big_file_id
                        photo_path = c.download_media(file_id)
                        button = InlineKeyboardMarkup(
                            [[InlineKeyboardButton(owner.first_name, user_id=owner.id)]]
                        )
                        m.reply_photo(
                            photo=photo_path, caption=caption, reply_markup=button
                        )
                        os.remove(photo_path)
                    except:
                        button = InlineKeyboardMarkup(
                            [[InlineKeyboardButton(owner.first_name, user_id=owner.id)]]
                        )
                        m.reply(caption, reply_markup=button)
                else:
                    button = InlineKeyboardMarkup(
                        [[InlineKeyboardButton(owner.first_name, user_id=owner.id)]]
                    )
                    m.reply(caption, reply_markup=button)

    if text == "اطردني":
        if r.get(f"{m.chat.id}:enableKickMe:{Dev_Zaid}"):
            get = m.chat.get_member(m.from_user.id)
            if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                return m.reply(f"{k} ممنوع طرد الحلوين")
            if admin_pls(m.from_user.id, m.chat.id):
                return m.reply(f"{k} ممنوع طرد الحلوين")
            else:
                m.reply(
                    f"طردتك يانفسية , وارسلت لك الرابط خاص تقدر ترجع متى مابغيت يامعقد"
                )
                m.chat.ban_member(m.from_user.id)
                time.sleep(0.5)
                c.unban_chat_member(m.chat.id, m.from_user.id)
                link = c.get_chat(m.chat.id).invite_link
                try:
                    c.send_message(
                        m.from_user.id,
                        f"{k} حبيبي النفسية رابط القروب الي طردتك منه: {link}",
                    )
                except:
                    pass
                return False

    if text == "الرابط":
        if not r.get(f"{m.chat.id}:disableLINK:{Dev_Zaid}"):
            if r.get(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}"):
                link = r.get(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}")
                if not link:
                    try:
                        new_link = c.create_chat_invite_link(m.chat.id, creates_join_request=True)
                        link = new_link.invite_link
                        r.set(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}", link)
                    except Exception as e:
                        return m.reply(f"{k} البوت ماعنده صلاحية دعوة المستخدمين عشان يسوي رابط طلب انضمام.")
                return m.reply(f"[{m.chat.title}]({link})", disable_web_page_preview=True)
            else:
                link = c.get_chat(m.chat.id).invite_link
                if not link:
                    try:
                        link = c.export_chat_invite_link(m.chat.id)
                    except:
                        pass
                return m.reply(f"[{m.chat.title}]({link})", disable_web_page_preview=True)


    if text == "تعطيل الرابط العادي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if m.chat.username:
            return m.reply(f"{k} ما تقدر تعطل الرابط العادي بقروب عام (له يوزر)، لازم يكون خاص.")
        try:
            new_link = c.create_chat_invite_link(m.chat.id, creates_join_request=True)
            r.set(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}", new_link.invite_link)
            r.set(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}", 1)
            # Try to revoke the normal link by generating a new primary one and not giving it out
            # Or just export it so old one dies, though it's optional.
            c.export_chat_invite_link(m.chat.id)
            return m.reply(f"{k} ابشر عطلت الرابط العادي وصار يعطي رابط طلب انضمام فقط\n☆")
        except Exception as e:
            return m.reply(f"{k} البوت ماعنده صلاحية كافية (إضافة مشرفين/إضافة مستخدمين) عشان يسوي رابط طلب.")

    if text == "تفعيل الرابط العادي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        r.delete(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}")
        return m.reply(f"{k} ابشر فعلت الرابط العادي\n☆")

    if text == "انشاء رابط":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        link = c.get_chat(m.chat.id).invite_link
        c.revoke_chat_invite_link(m.chat.id, link)
        return m.reply(f'{k} ابشر سويت رابط جديد ارسل "الرابط"')

    if text.startswith("@all") or text.startswith("تاك"):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if r.get(f"{m.chat.id}:disableALL:{Dev_Zaid}"):
            return m.reply("المنشن معطل")
        if r.get(f"{m.chat.id}:inMention:{Dev_Zaid}"):
            return False
        if r.get(f"{m.chat.id}:inMentionWAIT:{Dev_Zaid}"):
            get = r.ttl(f"{m.chat.id}:inMentionWAIT:{Dev_Zaid}")
            tm = time.strftime("%M:%S", time.gmtime(get))
            return m.reply(f"{k} سويت منشن من شوي تعال بعد {tm}")
        else:
            if len(text.split()) > 1:
                reason = text.split(None, 1)[1]
            else:
                reason = ""
            users_list = []
            r.set(f"{m.chat.id}:inMention:{Dev_Zaid}", 1)
            msg_to_reply = m.reply_to_message.id if m.reply_to_message else None
            m.reply(f"{k} بسوي منشن يحلو ، اذا تبي توقفه ارسل `/Cancel` او `ايقاف`")
            for mm in m.chat.get_members(limit=150):
                if mm.user and not mm.user.is_deleted and not mm.user.is_bot:
                    users_list.append(mm.user.mention)
            final_list = [users_list[x : x + 5] for x in range(0, len(users_list), 5)]
            ftext = f"{reason}\n\n"
            for a in final_list:
                for i in a:
                    if not r.get(f"{m.chat.id}:inMention:{Dev_Zaid}"):
                        return False
                    ftext += f"{i} , "
                c.send_message(m.chat.id, ftext, reply_to_message_id=msg_to_reply)
                ftext = f"{reason}\n\n"
            r.delete(f"{m.chat.id}:inMention:{Dev_Zaid}")
            r.set(f"{m.chat.id}:inMentionWAIT:{Dev_Zaid}", 1, ex=1200)

    if text.lower() == "/cancel" or text == "ايقاف":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:inMention:{Dev_Zaid}"):
                return m.reply(f"{k} مو قاعده اسوي منشن ركز")
            else:
                r.delete(f"{m.chat.id}:inMention:{Dev_Zaid}")
                return m.reply("ابشر وقفت المنشن")

    if text == "منشن":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        return m.reply("استخدم امر\n@all مع الكلام")

    if text == "تعطيل المنشن":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableALL:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} المشن معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableALL:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت المنشن\n☆"
                )

    if text == "تفعيل المنشن":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableALL:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} المنشن مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableALL:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت المنشن\n☆"
                )

    if text == "تعطيل الترحيب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableWelcome:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترحيب معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableWelcome:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الترحيب\n☆"
                )

    if text == "تفعيل الترحيب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableWelcome:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترحيب مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableWelcome:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الترحيب\n☆"
                )

    if text == "تعطيل الترحيب بالصورة" or text == "تعطيل الترحيب بالصوره":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableWelcomep:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترحيب بالصورة من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableWelcomep:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الترحيب بالصورة\n☆"
                )

    if text == "تفعيل الترحيب بالصورة" or text == "تفعيل الترحيب بالصوره":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableWelcomep:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترحيب بالصورة مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableWelcomep:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الترحيب بالصورة\n☆"
                )

    if text == "تعطيل الرابط":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableLINK:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الرابط معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableLINK:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الرابط\n☆"
                )

    if text == "تفعيل الرابط":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableLINK:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الرابط مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableLINK:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الرابط\n☆"
                )

    if text == "تعطيل البايو":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableBio:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} البايو معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableBio:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت البايو\n☆"
                )

    if text == "تفعيل البايو":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableBio:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} البايو مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableBio:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت البايو\n☆"
                )

    if text == "تعطيل اطردني":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:enableKickMe:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اطردني معطل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:enableKickMe:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت اطردني\n☆"
                )

    if text == "تفعيل اطردني":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:enableKickMe:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اطردني مفعل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:enableKickMe:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت اطردني\n☆"
                )

    if text == "تعطيل التحقق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:enableVerify:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التحقق معطل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:enableVerify:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت التحقق\n☆"
                )

    if text == "تفعيل التحقق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:enableVerify:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التحقق مفعل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:enableVerify:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت التحقق\n☆"
                )

    if text == "تعطيل انطقي" or text == "تعطيل انطق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableSay:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} انطقي معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableSay:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت انطقي\n☆"
                )

    if text == "تفعيل انطقي" or text == "تفعيل انطق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableSay:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} انطقي مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableSay:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت انطقي\n☆"
                )

    if text.startswith("انطق "):
        if not r.get(f"{m.chat.id}:disableSay:{Dev_Zaid}"):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return m.reply("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            """
         det = translator.detect(txt).lang.lower()
         if det == 'fa' or det == 'ar':
           lang = 'ar'
         else:
           lang = det
         """
            id = random.randint(999, 10000)
            """
         o = gtts.gTTS(text=txt, lang="ar", slow=False)
         o.save(f'zaid{id}.mp3')
         """
            with open(f"zaid{id}.mp3", "wb") as f:
                try:
                    c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                f.write(
                    requests.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}&model=3"
                    ).content
                )
            """
         audio = MP3(f'zaid{id}.mp3')
         duration=int(audio.info.length)
         os.rename(f'zaid{id}.mp3',f'zaid{id}.ogg')
         TelegramBot.send_voice(
         m.chat.id,
         voice,
         caption=f'الكلمة: {txt}',
         duration=duration
         )
         """
            try:
                c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            os.system(
                f"ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg"
            )
            try:
                c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            m.reply_voice(f"zaid{id}.ogg", caption=f"الكلمة: {txt}")
            """
         voice = open(f'zaid{id}.ogg','rb')
         url = f"https://api.telegram.org/bot{c.bot_token}/sendVoice"
         response=requests.post(url, data={'chat_id': m.chat.id,'caption':f'الكلمة: {txt}','reply_to_message_id':m.id}, files={'voice': voice})
         os.remove(f'zaid{id}.ogg')
         """
            os.remove(f"zaid{id}.ogg")
            os.remove(f"zaid{id}.mp3")
            return True

    if text.startswith("انطقي "):
        if not r.get(f"{m.chat.id}:disableSay:{Dev_Zaid}"):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return m.reply("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            """
         det = translator.detect(txt).lang.lower()
         if det == 'fa' or det == 'ar':
           lang = 'ar'
         else:
           lang = det
         """
            id = random.randint(999, 10000)
            """
         o = gtts.gTTS(text=txt, lang="ar", slow=False)
         o.save(f'zaid{id}.mp3')
         """
            with open(f"zaid{id}.mp3", "wb") as f:
                try:
                    c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                f.write(
                    requests.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}"
                    ).content
                )
            """
         audio = MP3(f'zaid{id}.mp3')
         duration=int(audio.info.length)
         os.rename(f'zaid{id}.mp3',f'zaid{id}.ogg')
         TelegramBot.send_voice(
         m.chat.id,
         voice,
         caption=f'الكلمة: {txt}',
         duration=duration
         )
         """
            try:
                c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            os.system(
                f"ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg"
            )
            try:
                c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            m.reply_voice(f"zaid{id}.ogg", caption=f"الكلمة: {txt}")
            """
         voice = open(f'zaid{id}.ogg','rb')
         url = f"https://api.telegram.org/bot{c.bot_token}/sendVoice"
         response=requests.post(url, data={'chat_id': m.chat.id,'caption':f'الكلمة: {txt}','reply_to_message_id':m.id}, files={'voice': voice})
         os.remove(f'zaid{id}.ogg')
         """
            os.remove(f"zaid{id}.ogg")
            os.remove(f"zaid{id}.mp3")
            return True

    if (
        (text == "وش يقول" or text == "وش تقول؟")
        and m.reply_to_message
        and m.reply_to_message.voice
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return m.reply("حجمه اكثر من ٢٠ ميجابايت، توكل")
        id = random.randint(99, 1000)
        voice = m.reply_to_message.download(f"./zaid{id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = sound.export(voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            text = s.recognize_google(audio_source, language="ar-SA")
        except Exception as e:
            print(e)
            os.remove(f"zaid{id}.wav")
            return m.reply("عجزت افهم وش يقول ")
        os.remove(f"zaid{id}.wav")
        return m.reply(f"يقول : {text}")

    if (
        (text == "zaid" or text == "زوز")
        and m.reply_to_message
        and m.reply_to_message.voice
        and m.from_user.id == 6168217372
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return m.reply("حجمه اكثر من ٢٠ ميجابايت، توكل")
        id = random.randint(99, 1000)
        voice = m.reply_to_message.download(f"./zaid{id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = sound.export(voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            text = s.recognize_google(audio_source, language="en-US")
        except Exception as e:
            print(e)
            os.remove(f"zaid{id}.wav")
            return m.reply("عجزت افهم وش يقول ")
        os.remove(f"zaid{id}.wav")
        return m.reply(f"يقول : {text}")

    if text.startswith("منع "):
        if mod_pls(m.from_user.id, m.chat.id):
            noice = text.split(None, 1)[1]
            if r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}", noice):
                return m.reply(
                    f"{k} الكلمة ( {noice} ) موجودة بقائمة المنع",
                    disable_web_page_preview=True,
                )
            else:
                r.sadd(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}", noice)
                return m.reply(
                    f"{k} الكلمة ( {noice} ) اضفتها الى قائمة المنع",
                    disable_web_page_preview=True,
                )

    if text.startswith("الغاء منع ") and len(text.split()) > 2:
        if mod_pls(m.from_user.id, m.chat.id):
            noice = text.split(None, 2)[2]
            if not r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}", noice):
                return m.reply(
                    f"{k} الكلمة ( {noice} ) مو مضافة بقائمة المنع",
                    disable_web_page_preview=True,
                )
            else:
                r.srem(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}", noice)
                return m.reply(
                    f"{k} ابشر مسحت ( {noice} ) من قائمة المنع",
                    disable_web_page_preview=True,
                )

    if text == "منع" and m.reply_to_message and m.reply_to_message.media:
        if mod_pls(m.from_user.id, m.chat.id):
            rep = m.reply_to_message
            if rep.sticker:
                file_id = rep.sticker.file_id
                type = "sticker"
            if rep.animation:
                file_id = rep.animation.file_id
                type = "animation"
            if rep.photo:
                file_id = rep.photo.file_id
                type = "photo"
            if rep.video:
                file_id = rep.photo.file_id
                type = "video"
            if rep.voice:
                file_id = rep.voice.file_id
                type = "voice"
            if rep.audio:
                file_id = rep.audio.file_id
                type = "audio"
            if rep.document:
                file_id = rep.document.file_id
                type = "document"

            id = file_id[-6:]
            if r.get(f"{id}:NotAllow:{m.chat.id}{Dev_Zaid}"):
                return m.reply(f"{k} موجودة بقائمة المنع")
            else:
                r.set(f"{id}:NotAllow:{m.chat.id}{Dev_Zaid}", 1)
                r.sadd(
                    f"{m.chat.id}:NotAllowedList:{Dev_Zaid}",
                    f"file={id}&by={m.from_user.id}&type={type}&file_id={file_id}",
                )
                return m.reply(f"{k} واضفناها لقائمة المنع")

    if text == "الغاء منع" and m.reply_to_message and m.reply_to_message.media:
        if mod_pls(m.from_user.id, m.chat.id):
            rep = m.reply_to_message
            if rep.sticker:
                file_id = rep.sticker.file_id
                type = "sticker"
            if rep.animation:
                file_id = rep.animation.file_id
                type = "animation"
            if rep.photo:
                file_id = rep.photo.file_id
                type = "photo"
            if rep.video:
                file_id = rep.photo.file_id
                type = "video"
            if rep.voice:
                file_id = rep.voice.file_id
                type = "voice"
            if rep.audio:
                file_id = rep.audio.file_id
                type = "audio"
            if rep.document:
                file_id = rep.document.file_id
                type = "document"

            id = file_id[-6:]
            if not r.get(f"{id}:NotAllow:{m.chat.id}{Dev_Zaid}"):
                return m.reply(f"{k} مو موجودة بقائمة المنع")
            else:
                r.delete(f"{id}:NotAllow:{m.chat.id}{Dev_Zaid}")
                r.srem(
                    f"{m.chat.id}:NotAllowedList:{Dev_Zaid}",
                    f"file={id}&by={m.from_user.id}&type={type}&file_id={file_id}",
                )
                return m.reply(f"{k} ابشر شلتها من قائمه المنع")

    if text == "منع" and m.reply_to_message and not m.reply_to_message.media:
        if mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} المنع بالرد فقط للوسائط")

    if text == "قائمه المنع" or text == "قائمة المنع":
        text1 = "الكلمات الممنوعة:\n"
        text2 = "الوسائط الممنوعة:\n"
        count = 1
        count2 = 1
        if mod_pls(m.from_user.id, m.chat.id):
            if not r.smembers(
                f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"
            ) and not r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                return m.reply(f"{k} مافي شي ممنوع")
            else:
                if not r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                    text1 += "لايوجد"
                else:
                    for a in r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                        text1 += f"{count} - {a}\n"
                        count += 1
                if not r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                    text2 += "لايوجد"
                else:
                    for a in r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                        g = a
                        id = g.split("file=")[1].split("&")[0]
                        by = g.split("by=")[1].split("&")[0]
                        type = g.split("type=")[1].split("&")[0]
                        text2 += (
                            f"{count2} - (`{id}`) ࿓ ( [{type}](tg://user?id={by}) )\n"
                        )
                return m.reply(f"{text1}\n{text2}", disable_web_page_preview=True)

    if text == "مسح قائمه المنع" or text == "مسح قائمة المنع":
        if mod_pls(m.from_user.id, m.chat.id):
            if not r.smembers(
                f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"
            ) and not r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                return m.reply(f"{k} مافي شي ممنوع")
            else:
                if r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                    r.delete(f"{m.chat.id}:NotAllowedListText:{Dev_Zaid}")
                if r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                    for a in r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}"):
                        file_id = a.split("file=")[1].split("&by=")[0]
                        r.delete(f"{file_id}:NotAllow:{m.chat.id}{Dev_Zaid}")
                r.delete(f"{m.chat.id}:NotAllowedList:{Dev_Zaid}")
                return m.reply(f"{k} ابشر مسحت قائمة المنع")

    if text == "قفل الكل":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if (
                r.get(f"{m.chat.id}:mute:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} كل شي مقفل يالطيب!\n☆"
                )
            else:
                m.reply(f"{k} من 「 {m.from_user.mention} 」 \n{k} ابشر قفلت كل شي\n☆")
                r.set(f"{m.chat.id}:mute:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockJoin:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockChannels:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockEdit:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockEditM:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockVoice:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockVideo:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockNot:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockStickers:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockFiles:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockPersian:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockUrls:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockHashtags:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockMessages:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockTags:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockBots:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockSpam:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockInline:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockForward:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockAudios:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return False

    if text == "فتح الكل":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if (
                not r.get(f"{m.chat.id}:mute:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} كل شي مفتوح يالطيب!\n☆"
                )
            else:
                m.reply(f"{k} من 「 {m.from_user.mention} 」 \n{k} ابشر فتحت كل شي\n☆")
                r.delete(f"{m.chat.id}:mute:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockJoin:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockEdit:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockNot:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockHashtags:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockBots:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockInline:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockKFR:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
                return False


    if text == "تفعيل الوضع الليلي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
                return m.reply(f"{k} من「 {m.from_user.mention} 」\n{k} الوضع الليلي مفعل من قبل\n☆")
            else:
                r.set(f"{m.chat.id}:NightMode:{Dev_Zaid}", 1)
                return m.reply(f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الوضع الليلي الميديا بتنحذف\n☆")

    if text == "تعطيل الوضع الليلي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
                return m.reply(f"{k} من「 {m.from_user.mention} 」\n{k} الوضع الليلي معطل من قبل\n☆")
            else:
                r.delete(f"{m.chat.id}:NightMode:{Dev_Zaid}")
                return m.reply(f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الوضع الليلي\n☆")

    if text == "تفعيل الحماية" or text == "تفعيل الحمايه":
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if (
                r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                and r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} الحماية مفعله من قبل\n☆"
                )
            else:
                m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} ابشر فعلت الحمايه\n☆"
                )

                r.set(f"{m.chat.id}:lockChannels:{Dev_Zaid}", 1)
                r.delete(f"{m.chat.id}:disableWarn:{Dev_Zaid}")
                r.set(f"{m.chat.id}:lockVoice:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockVideo:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockStickers:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockFiles:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockPersian:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockUrls:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockTags:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockSpam:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockForward:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockAudios:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                r.set(f"{m.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return False

    if text == "تعطيل الحماية" or text == "تعطيل الحمايه":
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if (
                r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                and not r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} الحماية معطله من قبل\n☆"
                )
            else:
                m.reply(
                    f"{k} من 「 {m.from_user.mention} 」 \n{k} ابشر عطلت الحمايه\n☆"
                )

                r.delete(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                r.delete(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
                return False

    if text == "قفل الدردشة" or text == "قفل الدردشه" or text == "قفل الشات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:mute:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الشات"))
            else:
                r.set(f"{m.chat.id}:mute:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الشات"))

    if text == "فتح الدردشة" or text == "فتح الدردشه" or text == "فتح الشات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:mute:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الشات"))
            else:
                r.delete(f"{m.chat.id}:mute:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الشات"))

    if text == "قفل التعديل":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "التعديل"))
            else:
                r.set(f"{m.chat.id}:lockEdit:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "التعديل"))

    if text == "فتح التعديل":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "التعديل"))
            else:
                r.delete(f"{m.chat.id}:lockEdit:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "التعديل"))

    if text == "قفل تعديل الميديا":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "تعديل الميديا"))
            else:
                r.set(f"{m.chat.id}:lockEditM:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "تعديل الميديا"))

    if text == "فتح تعديل الميديا":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "تعديل الميديا"))
            else:
                r.delete(f"{m.chat.id}:lockEditM:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "تعديل الميديا"))

    if text == "قفل الفويسات" or text == "قفل البصمات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الفويس"))
            else:
                r.set(f"{m.chat.id}:lockVoice:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الفويس"))

    if text == "فتح الفويسات" or text == "فتح البصمات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الفويس"))
            else:
                r.delete(f"{m.chat.id}:lockVoice:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الفويس"))

    if text == "قفل الفيديو" or text == "قفل الفيديوهات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الفيديو"))
            else:
                r.set(f"{m.chat.id}:lockVideo:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الفيديو"))

    if text == "فتح الفيديو" or text == "فتح الفيديوهات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الفيديو"))
            else:
                r.delete(f"{m.chat.id}:lockVideo:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الفيديو"))

    if text == "قفل الاشعارات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الاشعارات"))
            else:
                r.set(f"{m.chat.id}:lockNot:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الاشعارات"))

    if text == "فتح الاشعارات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الاشعارات"))
            else:
                r.delete(f"{m.chat.id}:lockNot:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الاشعارات"))

    if text == "قفل الصور":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الصور"))
            else:
                r.set(f"{m.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الصور"))

    if text == "فتح الصور":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الصور"))
            else:
                r.delete(f"{m.chat.id}:lockPhoto:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الصور"))

    if text == "قفل الملصقات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الملصقات"))
            else:
                r.set(f"{m.chat.id}:lockStickers:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الملصقات"))

    if text == "فتح الملصقات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الملصقات"))
            else:
                r.delete(f"{m.chat.id}:lockStickers:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الملصقات"))

    if text == "قفل الفارسيه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الفارسيه"))
            else:
                r.set(f"{m.chat.id}:lockPersian:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الفارسيه"))

    if text == "فتح الفارسيه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الفارسيه"))
            else:
                r.delete(f"{m.chat.id}:lockPersian:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الفارسيه"))

    if text == "قفل الملفات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الملفات"))
            else:
                r.set(f"{m.chat.id}:lockFiles:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الملفات"))

    if text == "فتح الملفات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الملفات"))
            else:
                r.delete(f"{m.chat.id}:lockFiles:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الملفات"))

    if text == "قفل المتحركات" or text == "قفل المتحركه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "المتحركات"))
            else:
                r.set(f"{m.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "المتحركات"))

    if text == "فتح المتحركات" or text == "فتح المتحركه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "المتحركات"))
            else:
                r.delete(f"{m.chat.id}:lockAnimations:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "المتحركات"))

    if text == "قفل الروابط":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الروابط"))
            else:
                r.set(f"{m.chat.id}:lockUrls:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الروابط"))

    if text == "فتح الروابط":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الروابط"))
            else:
                r.delete(f"{m.chat.id}:lockUrls:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الروابط"))

    if text == "قفل الهشتاق" or text == "قفل الهاشتاق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الهاشتاق"))
            else:
                r.set(f"{m.chat.id}:lockHashtags:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الهاشتاق"))

    if text == "فتح الهشتاق" or text == "فتح الهاشتاق":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الهاشتاق"))
            else:
                r.delete(f"{m.chat.id}:lockHashtags:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الهاشتاق"))

    if text == "قفل البوتات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "البوتات"))
            else:
                r.set(f"{m.chat.id}:lockBots:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "البوتات"))

    if text == "فتح البوتات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockBots:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "البوتات"))
            else:
                r.delete(f"{m.chat.id}:lockBots:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "البوتات"))

    if text == "قفل البوتات بالطرد":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockBotsKick:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "البوتات بالطرد"))
            else:
                r.set(f"{m.chat.id}:lockBotsKick:{Dev_Zaid}", 1)
                m.reply(lock.format(k, m.from_user.mention, k, "البوتات بالطرد"))
                co = 0
                try:
                    for mm in m.chat.get_members(filter=ChatMembersFilter.BOTS):
                        if not admin_pls(mm.user.id, m.chat.id):
                            try:
                                m.chat.ban_member(mm.user.id)
                                m.chat.unban_member(mm.user.id)
                                co += 1
                            except:
                                pass
                except:
                    pass
                if co > 0:
                    m.reply(f"{k} تم طرد ( {co} ) بوت ليس لديه إشراف\n☆")
                return True

    if text == "فتح البوتات بالطرد":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockBotsKick:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "البوتات بالطرد"))
            else:
                r.delete(f"{m.chat.id}:lockBotsKick:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "البوتات بالطرد"))

    if text == "قفل اليوزرات" or text == "قفل المنشن":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "اليوزرات"))
            else:
                r.set(f"{m.chat.id}:lockTags:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "اليوزرات"))

    if text == "فتح اليوزرات" or text == "فتح المنشن":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "اليوزرات"))
            else:
                r.delete(f"{m.chat.id}:lockTags:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "اليوزرات"))

    """
   if text == 'قفل الكفر' or text == 'قفل الشيعه' or text == 'قفل الشيعة':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if r.get(f'{m.chat.id}:lockKFR:{Dev_Zaid}'):
         return m.reply(locknn.format(k,m.from_user.mention,k,'الكفر'))
       else:
         r.set(f'{m.chat.id}:lockKFR:{Dev_Zaid}',1)
         return m.reply(lock.format(k,m.from_user.mention,k,'الكفر'))

   if text == 'فتح الكفر' or text == 'فتح الشيعه' or text == 'فتح الشيعة':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.get(f'{m.chat.id}:lockKFR:{Dev_Zaid}'):
         return m.reply(Openn2.format(k,m.from_user.mention,k,'الكفر'))
       else:
         r.delete(f'{m.chat.id}:lockKFR:{Dev_Zaid}')
         return m.reply(Open.format(k,m.from_user.mention,k,'الكفر'))
   """

    if text == "قفل الإباحي" or text == "قفل الاباحي":
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الإباحي"))
            else:
                r.set(f"{m.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الإباحي"))

    if text == "فتح الإباحي" or text == "فتح الاباحي":
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockNSFW:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "االإباحي"))
            else:
                r.delete(f"{m.chat.id}:lockNSFW:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الإباحي"))

    if text == "قفل الكلام الكثير" or text == "قفل الكلايش":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الكلام الكثير"))
            else:
                r.set(f"{m.chat.id}:lockMessages:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الكلام الكثير"))

    if text == "فتح الكلام الكثير" or text == "فتح الكلايش":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockMessages:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الكلام الكثير"))
            else:
                r.delete(f"{m.chat.id}:lockMessages:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الكلام الكثير"))


    if text.startswith("وضع التكرار "):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        count = text.replace("وضع التكرار ", "")
        if not count.isdigit():
            return m.reply(f"{k} أرسل العدد بالأرقام فقط\n☆")
        if int(count) < 2:
            return m.reply(f"{k} العدد لازم يكون 2 أو أكثر\n☆")
        r.set(f"{m.chat.id}:spamLimit:{Dev_Zaid}", int(count))
        return m.reply(f"{k} ابشر تم وضع حد التكرار على {count}\n☆")

    if text == "قفل التكرار بالكتم":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "التكرار بالكتم"))
            else:
                r.set(f"{m.chat.id}:lockSpam:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "التكرار بالكتم"))

    if text == "قفل التكرار":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "التكرار"))
            else:
                r.set(f"{m.chat.id}:lockSpam:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "التكرار"))

    if text == "فتح التكرار":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "التكرار"))
            else:
                r.delete(f"{m.chat.id}:lockSpam:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "التكرار"))

    if text == "قفل التوجيه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "التوجيه"))
            else:
                r.set(f"{m.chat.id}:lockForward:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "التوجيه"))

    if text == "فتح التوجيه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "التوجيه"))
            else:
                r.delete(f"{m.chat.id}:lockForward:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "التوجيه"))

    if text == "قفل الانلاين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الانلاين"))
            else:
                r.set(f"{m.chat.id}:lockInline:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الانلاين"))

    if text == "فتح الانلاين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الانلاين"))
            else:
                r.delete(f"{m.chat.id}:lockInline:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الانلاين"))

    if text == "قفل السب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "السب"))
            else:
                r.set(f"{m.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "السب"))

    if text == "فتح السب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "السب"))
            else:
                r.delete(f"{m.chat.id}:lockSHTM:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "السب"))

    if text == "قفل الاضافه" or text == "قفل الاضافة" or text == "قفل الجهات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "الاضافه"))
            else:
                r.set(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الاضافه"))

    if text == "فتح الاضافه" or text == "فتح الاضافة" or text == "فتح الجهات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "الاضافه"))
            else:
                r.delete(f"{m.chat.id}:lockaddContacts:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الاضافه"))

    if text == "قفل دخول البوتات" or text == "قفل الوهمي" or text == "قفل الايراني":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "دخول البوتات"))
            else:
                r.set(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "دخول البوتات"))

    if text == "فتح دخول البوتات" or text == "فتح الوهمي" or text == "فتح الايراني":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "دخول البوتات"))
            else:
                r.delete(f"{m.chat.id}:lockJoinPersian:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "دخول البوتات"))

    if text == "قفل الصوت":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الصوت"))
            else:
                r.set(f"{m.chat.id}:lockAudios:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الصوت"))

    if text == "فتح الصوت":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الصوت"))
            else:
                r.delete(f"{m.chat.id}:lockAudios:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الصوت"))

    if text == "قفل القنوات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}"):
                return m.reply(locknn.format(k, m.from_user.mention, k, "القنوات"))
            else:
                r.set(f"{m.chat.id}:lockChannels:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "القنوات"))

    if text == "فتح القنوات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockChannels:{Dev_Zaid}"):
                return m.reply(Openn2.format(k, m.from_user.mention, k, "القنوات"))
            else:
                r.delete(f"{m.chat.id}:lockChannels:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "القنوات"))

    if text == "قفل الدخول":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "الدخول"))
            else:
                r.set(f"{m.chat.id}:lockJoin:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "الدخول"))

    if text == "فتح الدخول":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:lockJoin:{Dev_Zaid}"):
                return m.reply(Openn.format(k, m.from_user.mention, k, "الدخول"))
            else:
                r.delete(f"{m.chat.id}:lockJoin:{Dev_Zaid}")
                return m.reply(Open.format(k, m.from_user.mention, k, "الدخول"))

    if text == "تعطيل التحذير":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التحذير معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableWarn:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت التحذير\n☆"
                )

    if text == "تفعيل التحذير":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التحذير مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableWarn:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت التحذير\n☆"
                )

    if text == "تعطيل اليوتيوب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableYT:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اليوتيوب معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableYT:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت اليوتيوب\n☆"
                )

    if text == "تفعيل اليوتيوب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableYT:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اليوتيوب مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableYT:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت اليوتيوب\n☆"
                )

    if text == "تعطيل الساوند":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableSound:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الساوند معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableSound:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الساوند\n☆"
                )

    if text == "تفعيل الساوند":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableSound:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الساوند مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableSound:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الساوند\n☆"
                )

    if text == "تعطيل الانستا":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableINSTA:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الانستا معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableINSTA:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الانستا\n☆"
                )

    if text == "تفعيل الانستا":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableINSTA:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الانستا مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableINSTA:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الانستا\n☆"
                )

    if text == "تعطيل اهمس":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableWHISPER:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اهمس معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableWHISPER:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت اهمس\n☆"
                )

    if text == "تفعيل اهمس":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableWHISPER:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} اهمس مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableWHISPER:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت اهمس\n☆"
                )

    if text == "تعطيل التيك":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableTik:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التيك معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableTik:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت التيك\n☆"
                )

    if text == "تفعيل التيك":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableTik:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التيك مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableTik:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت التيك\n☆"
                )

    if text == "تعطيل شازام":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableShazam:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} شازام معطل من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableShazam:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت شازام\n☆"
                )

    if text == "تفعيل شازام":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableShazam:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} شازام مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableShazam:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت شازام\n☆"
                )

    if text == "تعطيل الالعاب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableGames:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الالعاب معطله من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableGames:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الالعاب\n☆"
                )

    if text == "تفعيل الالعاب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableGames:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الالعاب مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableGames:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الالعاب\n☆"
                )

    if text == "تعطيل الترجمة" or text == "تعطيل الترجمه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترجمه معطله من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableTrans:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الترجمه\n☆"
                )

    if text == "تفعيل الترجمة" or text == "تفعيل الترجمه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الترجمه مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableTrans:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الترجمه\n☆"
                )

    if text == "تعطيل التسلية" or text == "تعطيل التسليه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:disableFun:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التسلية معطله من قبل\n☆"
                )
            else:
                r.set(f"{m.chat.id}:disableFun:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت التسلية\n☆"
                )

    if text == "تفعيل التسلية" or text == "تفعيل التسليه":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:disableFun:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التسلية مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{m.chat.id}:disableFun:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت التسلية\n☆"
                )

    if text == "تعطيل الاشتراك":
        if not dev2_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        else:
            if r.get(f"disableSubscribe:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الاشتراك الاجباري معطل من قبل\n☆"
                )
            else:
                r.set(f"disableSubscribe:{Dev_Zaid}", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الاشتراك الاجباري\n☆"
                )

    if text == "قناة الاشتراك":
        if not dev2_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        ch = r.get(f"forceChannel:{Dev_Zaid}") or "مافي قناة"
        return m.reply(f"{k} قناة الاشتراك هي ( {ch} )")

    if text.startswith("وضع قناة @"):
        if not dev2_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        username = text.split("@")[1]
        try:
            chat = c.get_chat(username)
        except:
            return m.reply(f"{k} حدث خطأ")
        r.set(f"forceChannel:{Dev_Zaid}", "@" + username)
        return m.reply(f"{k} تم تعيين القناة بنجاح")

    if text == "تفعيل الاشتراك":
        if not dev2_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        else:
            if not r.get(f"disableSubscribe:{Dev_Zaid}"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} الاشتراك الاجباري مفعل من قبل\n☆"
                )
            else:
                r.delete(f"disableSubscribe:{Dev_Zaid}")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الاشتراك الاجباري\n☆"
                )

    if (
        text == "/ar"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
            text = m.reply_to_message.text or m.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target=ar&text={text}"
            ).json()["result"]["translate"]
            m.reply(f"`{translation}`")

    if (
        text == "/en"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
            text = m.reply_to_message.text or m.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target=en&text={text}"
            ).json()["result"]["translate"]
            m.reply(f"`{translation}`")

    if (
        text == "ترجمه"
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
            text = m.reply_to_message.text or m.reply_to_message.caption
            en = requests.get(
                f"https://hozory.com/translate/?target=en&text={text}"
            ).json()["result"]["translate"]
            ar = requests.get(
                f"https://hozory.com/translate/?target=ar&text={text}"
            ).json()["result"]["translate"]
            ru = requests.get(
                f"https://hozory.com/translate/?target=ru&text={text}"
            ).json()["result"]["translate"]
            zh = requests.get(
                f"https://hozory.com/translate/?target=zh&text={text}"
            ).json()["result"]["translate"]
            fr = requests.get(
                f"https://hozory.com/translate/?target=fr&text={text}"
            ).json()["result"]["translate"]
            du = requests.get(
                f"https://hozory.com/translate/?target=nl&text={text}"
            ).json()["result"]["translate"]
            tr = requests.get(
                f"https://hozory.com/translate/?target=tr&text={text}"
            ).json()["result"]["translate"]
            txt = f"🇷🇺 : \n {ru}\n\n🇨🇳 : \n {zh}\n\n🇫🇷 :\n {fr}\n\n🇩🇪 :\n {du}\n\n🇹🇷 : \n{tr}"
            return m.reply(txt)

    if (
        text.startswith("ترجمه ")
        and m.reply_to_message
        and (m.reply_to_message.text or m.reply_to_message.caption)
    ):
        if not r.get(f"{m.chat.id}:disableTrans:{Dev_Zaid}"):
            lang = text.split()[1]
            text = m.reply_to_message.text or m.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target={lang}&text={text}"
            ).json()["result"]["translate"]
            m.reply(f"`{translation}`")

    if text == "ابلاغ" and m.reply_to_message:
        text = f"{k} تم ابلاغ المشرفين"
        cc = 0
        for mm in c.get_chat_members(
            m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if not mm.user.is_deleted and not mm.user.is_bot:
                cc += 1
                text += f"[⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮](tg://user?id={mm.user.id})"
        if cc == 0:
            return False
        return m.reply(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚠️", callback_data="delAdminMSG")]]
            ),
        )

    if text == "المقيدين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            cc = 1
            text = "المقيدين:\n\n"
            for mm in c.get_chat_members(
                m.chat.id, filter=ChatMembersFilter.RESTRICTED
            ):
                if co == 100:
                    break
                if not mm.user.is_deleted:
                    co += 1
                    user = (
                        f"@{mm.user.username}"
                        if mm.user.username
                        else f"[@{channel}](tg://user?id={mm.user.id})"
                    )
                    text += f"{cc} ➣ {user} ☆ ( `{mm.user.id}` )\n"
                    cc += 1
            text += "☆"
            if co == 0:
                return m.reply(f"{k} مافيه مقيديين")
            else:
                return m.reply(text)

    if text == "مسح المقيدين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            for mm in c.get_chat_members(
                m.chat.id, filter=ChatMembersFilter.RESTRICTED
            ):
                co += 1
                c.restrict_chat_member(
                    m.chat.id,
                    mm.user.id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_pin_messages=True,
                    ),
                )
            if co == 0:
                return m.reply(f"{k} مافيه مقيديين")
            else:
                return m.reply(f"{k} ابشر مسحت ( {co} ) من المقيدين")

    if text == "تثبيت" and m.reply_to_message:
        if mod_pls(m.from_user.id, m.chat.id):
            m.reply_to_message.pin(disable_notification=False)
            m.reply(f"{k} ابشر ثبتت الرسالة ")

    if text == "الغاء التثبيت" and m.reply_to_message:
        if mod_pls(m.from_user.id, m.chat.id):
            m.reply_to_message.unpin()
            m.reply(f"{k} ابشر لغيت تثبيت الرسالة ")

    if text.startswith("تقييد ") and len(text.split()) == 2:
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = m.chat.get_member(user)
                if m.from_user.id == get.user.id:
                    return m.reply("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, m.chat.id):
                    rank = get_rank(get.user.id, m.chat.id)
                    return m.reply(f"{k} هييه مايمديك تقييد {rank} ياورع!")
                if get.status == ChatMemberStatus.RESTRICTED:
                    return m.reply(f"「 {get.user.mention} 」 \n{k} مقيد من قبل\n☆")
            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            c.restrict_chat_member(
                m.chat.id, get.user.id, ChatPermissions(can_send_messages=False)
            )
            r.set(f'{m.chat.id}:print:restrict:{get.user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
            bot_msg = m.reply(f"「 {get.user.mention} 」 \n{k} قييدته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):")
            data = {"action": "تقييد", "target_id": get.user.id, "mention": get.user.mention}
            r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
            return bot_msg

    if text == "تقييد" and m.reply_to_message and m.reply_to_message.from_user:
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            if m.from_user.id == m.reply_to_message.from_user.id:
                return m.reply("شفيك تبي تنزل نفسك")
            get = m.chat.get_member(m.reply_to_message.from_user.id)
            if pre_pls(m.reply_to_message.from_user.id, m.chat.id):
                rank = get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return m.reply(f"{k} هييه مايمديك تقييد {rank} ياورع!")
            if get.status == ChatMemberStatus.RESTRICTED:
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」 \n{k} مقيد من قبل\n☆"
                )
            c.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                ChatPermissions(can_send_messages=False),
            )
            r.set(f'{m.chat.id}:print:restrict:{m.reply_to_message.from_user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
            bot_msg = m.reply(
                f"「 {m.reply_to_message.from_user.mention} 」 \n{k} قييدته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):"
            )
            data = {"action": "تقييد", "target_id": m.reply_to_message.from_user.id, "mention": m.reply_to_message.from_user.mention}
            r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
            return bot_msg

    if (
        text.startswith("الغاء تقييد ")
        or text.startswith("الغاء التقييد ")
        and len(text.split()) == 3
    ):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            try:
                get = m.chat.get_member(user)
                if not get.status == ChatMemberStatus.RESTRICTED:
                    return m.reply(f"「 {get.user.mention} 」 \n{k} مو مقيد من قبل\n☆")
            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            c.restrict_chat_member(
                m.chat.id,
                get.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
            return m.reply(f"「 {get.user.mention} 」 \n{k} ابشر الغيت تقييده\n☆")

    if (
        text == "الغاء تقييد"
        or text == "الغاء التقييد"
        and m.reply_to_message
        and m.reply_to_message.from_user
    ):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            get = m.chat.get_member(m.reply_to_message.from_user.id)
            if not get.status == ChatMemberStatus.RESTRICTED:
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」 \n{k} مو مقيد من قبل\n☆"
                )
            c.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
            return m.reply(
                f"「 {m.reply_to_message.from_user.mention} 」 \n{k} ابشر الغيت تقييده\n☆"
            )

    # ===== أمر برنت - تقرير القيود =====
    if text == "برنت" and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        target_id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        return _print_report(c, m, target_id, mention, k)

    if text.startswith("برنت ") and len(text.split()) == 2:
        if not '@' in text and not re.findall('[0-9]+', text):
            return
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        user = text.split()[1]
        try:
            target_id = int(user)
        except:
            target_id = user.replace('@', '')
        try:
            get_user = c.get_users(str(target_id).lstrip('@'))
            target_id = get_user.id
            mention = f'[{get_user.first_name}](tg://user?id={get_user.id})'
        except:
            return m.reply(f'{k} مافيه يوزر كذا')
        return _print_report(c, m, target_id, mention, k)

    if text == "المحظورين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            cc = 1
            text = "المحظورين:\n\n"
            for mm in c.get_chat_members(m.chat.id, filter=ChatMembersFilter.BANNED):
                if co == 100:
                    break
                if mm.user:
                    if not mm.user.is_deleted:
                        co += 1
                        user = (
                            f"@{mm.user.username}"
                            if mm.user.username
                            else f"[@{channel}](tg://user?id={mm.user.id})"
                        )
                        text += f"{cc} ➣ {user} ☆ ( `{mm.user.id}` )\n"
                        cc += 1
                if mm.chat:
                    co += 1
                    user = f"@{mm.chat.username}"
                    text += f"{cc} ➣ {user} ☆ (`{mm.chat.id}`)\n"
                    cc += 1
            text += "☆"
            if co == 0:
                return m.reply(f"{k} مافيه محظورين")
            else:
                return m.reply(text)

    if text == "مسح المحظورين":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            co = 0
            for mm in c.get_chat_members(m.chat.id, filter=ChatMembersFilter.BANNED):
                if mm.user:
                    co += 1
                    c.unban_chat_member(m.chat.id, mm.user.id)
                if mm.chat:
                    co += 1
                    c.unban_chat_member(m.chat.id, mm.chat.id)
            if co == 0:
                return m.reply(f"{k} مافيه محظورين")
            else:
                return m.reply(f"{k} ابشر مسحت ( {co} ) من المحظورين")

    if text.startswith("حظر ") and len(text.split()) == 2:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = m.chat.get_member(user)
                if m.from_user.id == get.user.id:
                    return m.reply("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, m.chat.id):
                    rank = get_rank(get.user.id, m.chat.id)
                    return m.reply(f"{k} هييه مايمديك تحظر {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return m.reply(f"「 {get.user.mention} 」 \n{k} محظور من قبل\n☆")
            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            m.chat.ban_member(get.user.id)
            r.set(f'{m.chat.id}:print:ban:{get.user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
            bot_msg = m.reply(f"「 {get.user.mention} 」 \n{k} حظرته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):")
            data = {"action": "حظر", "target_id": get.user.id, "mention": get.user.mention}
            r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
            return bot_msg

    if text == "حظر" and m.reply_to_message and m.reply_to_message.from_user:
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            if m.from_user.id == m.reply_to_message.from_user.id:
                return m.reply("شفيك تبي تنزل نفسك")
            get = m.chat.get_member(m.reply_to_message.from_user.id)
            if pre_pls(m.reply_to_message.from_user.id, m.chat.id):
                rank = get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return m.reply(f"{k} هييه مايمديك تحظر {rank} ياورع!")
            if get.status == ChatMemberStatus.BANNED:
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」 \n{k} محظور من قبل\n☆"
                )
            m.chat.ban_member(m.reply_to_message.from_user.id)
            r.set(f'{m.chat.id}:print:ban:{m.reply_to_message.from_user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
            bot_msg = m.reply(
                f"「 {m.reply_to_message.from_user.mention} 」 \n{k} حظرته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):"
            )
            data = {"action": "حظر", "target_id": m.reply_to_message.from_user.id, "mention": m.reply_to_message.from_user.mention}
            r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
            return bot_msg

    if text == "طرد البوتات":
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            co = 0
            for mm in m.chat.get_members(filter=ChatMembersFilter.BOTS):
                try:
                    m.chat.ban_member(mm.user.id)
                    co += 1
                except:
                    pass
            if co == 0:
                return m.reply(f"{k} مافيه بوتات")
            else:
                return m.reply(f"{k} ابشر حظر ( {co} ) بوت")

    if text.startswith("طرد ") and len(text.split()) == 2:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = m.chat.get_member(user)
                if m.from_user.id == get.user.id:
                    return m.reply("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, m.chat.id):
                    rank = get_rank(get.user.id, m.chat.id)
                    return m.reply(f"{k} هييه مايمديك تطرد {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return m.reply(f"「 {get.user.mention} 」 \n{k} مطرود من قبل\n☆")
            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            m.chat.ban_member(get.user.id)
            m.chat.unban_member(get.user.id)
            bot_msg = m.reply(f"「 {get.user.mention} 」 \n{k} طردته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):")
            data = {"action": "طرد", "target_id": get.user.id, "mention": get.user.mention}
            r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
            r.set(f'{m.chat.id}:print:kick:{get.user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
            return bot_msg

    if text == "اهمس" and m.reply_to_message and m.reply_to_message.from_user:
        if r.get(f"{m.chat.id}:disableWHISPER:{Dev_Zaid}"):
            return m.reply(f"{k} امر اهمس معطل")
        user_id = m.reply_to_message.from_user.id
        if user_id == m.from_user.id:
            return m.reply(f"{k} مافيك تهمس لنفسك ياغبي")
        else:
            import uuid

            id = str(uuid.uuid4())[:6]
            a = m.reply(
                f"{k} تم تحديد الهمسة الى [ {m.reply_to_message.from_user.mention} ]",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"اهمس الى [ {m.reply_to_message.from_user.first_name[:25]} ]",
                                url=f"https://t.me/{c.me.username}?start=hmsa{id}",
                            )
                        ]
                    ]
                ),
            )
            data = {
                "from": m.from_user.id,
                "to": user_id,
                "chat": m.chat.id,
                "id": a.id,
            }
            # wsdb.set(str(id), data)
            wsdb.setex(key=id, ttl=3600, value=data)
            return True

    if text == "تعطيل التنظيف":
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            if not r.hget(Dev_Zaid + str(m.chat.id), "ena-clean"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التنظيف معطل من قبل\n☆"
                )
            else:
                r.hdel(Dev_Zaid + str(m.chat.id), "ena-clean")
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت التنظيف\n☆"
                )

    if text == "تفعيل التنظيف":
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            if r.hget(Dev_Zaid + str(m.chat.id), "ena-clean"):
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} التنظيف مفعل من قبل\n☆"
                )
            else:
                r.hset(Dev_Zaid + str(m.chat.id), "ena-clean", 1)
                return m.reply(
                    f"{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت التنظيف\n☆"
                )

    if re.search("^وضع وقت التنظيف [0-9]+$", text):
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            secs = int(text.split()[3])
            if secs > 3600 or secs < 60:
                return m.reply(
                    f"{k} عليك تحديد وقت التنظيف بالثواني من 60 الى 3600 ثانية"
                )
            else:
                r.hset(Dev_Zaid + str(m.chat.id), "clean-secs", secs)
                return m.reply(f"{k} تم تعيين وقت التنظيف ( {secs} ) ثانية")

    if text == "وقت التنظيف":
        if not gowner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            secs = r.hget(Dev_Zaid + str(m.chat.id), "clean-secs") or "60"
            return m.reply(f"`{secs}`")

    if text == "طرد" and m.reply_to_message and m.reply_to_message.from_user:
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                if m.from_user.id == m.reply_to_message.from_user.id:
                    return m.reply("شفيك تبي تنزل نفسك")
                get = m.chat.get_member(m.reply_to_message.from_user.id)
                if pre_pls(m.reply_to_message.from_user.id, m.chat.id):
                    rank = get_rank(m.reply_to_message.from_user.id, m.chat.id)
                    return m.reply(f"{k} هييه مايمديك تطرد {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return m.reply(
                        f"「 {m.reply_to_message.from_user.mention} 」 \n{k} مطرود من قبل\n☆"
                    )
                m.chat.ban_member(m.reply_to_message.from_user.id)
                bot_msg = m.reply(f"「 {m.reply_to_message.from_user.mention} 」 \n{k} طردته\n☆\n\nقم بالرد على هذه الرسالة لكتابة السبب (أو تجاهلها):")
                m.chat.unban_member(m.reply_to_message.from_user.id)
                data = {"action": "طرد", "target_id": m.reply_to_message.from_user.id, "mention": m.reply_to_message.from_user.mention}
                r.set(f"reason_req:{bot_msg.id}:{m.chat.id}", _json.dumps(data), ex=300)
                r.set(f'{m.chat.id}:print:kick:{m.reply_to_message.from_user.id}{Dev_Zaid}', _json.dumps({"id": m.from_user.id, "name": m.from_user.first_name, "time": int(time.time()), "reason": "لا يوجد"}))
                return bot_msg
            except:
                return m.reply(f"{k} العضو مو بالمجموعة")

    if (
        text.startswith("رفع الحظر ")
        or text.startswith("الغاء الحظر ")
        and len(text.split()) == 3
    ):
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            try:
                get = m.chat.get_member(user)
                if not get.status == ChatMemberStatus.BANNED:
                    return m.reply(f"「 {get.user.mention} 」 \n{k} مو محظور من قبل\n☆")
            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            m.chat.unban_member(get.user.id)
            r.delete(f'{m.chat.id}:print:ban:{get.user.id}{Dev_Zaid}')
            return m.reply(f"「 {get.user.mention} 」 \n{k} ابشر الغيت حظره\n☆")

    if (
        text == "رفع الحظر"
        or text == "الغاء الحظر"
        and m.reply_to_message
        and m.reply_to_message.from_user
    ):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                get = m.chat.get_member(m.reply_to_message.from_user.id)
                if not get.status == ChatMemberStatus.BANNED:
                    return m.reply(
                        f"「 {m.reply_to_message.from_user.mention} 」 \n{k} مو محظور من قبل\n☆"
                    )
                m.chat.unban_member(m.reply_to_message.from_user.id)
                r.delete(f'{m.chat.id}:print:ban:{m.reply_to_message.from_user.id}{Dev_Zaid}')
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」 \n{k} ابشر الغيت حظره\n☆"
                )
            except:
                return m.reply(f"{k} العضو مو بالمجموعة")

    if text.startswith("رفع القيود ") and len(text.split()) == 3:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            co = 0
            text = ""
            try:
                get = m.chat.get_member(user)
                if get.status == ChatMemberStatus.BANNED:
                    m.chat.unban_member(get.user.id)
                    text += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    c.restrict_chat_member(
                        m.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    text += "تقييد\n"
                    co += 1
                if r.get(f"{get.user.id}:mute:{m.chat.id}{Dev_Zaid}"):
                    r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_Zaid}")
                    r.srem(f"{m.chat.id}:listMUTE:{Dev_Zaid}", get.user.id)
                    text += "كتم\n"
                    co += 1
                if co > 0:
                    return m.reply(f"رفعت القيود التالية:\n{text}\n☆")
                else:
                    return m.reply(f"「 {get.user.mention} 」\n{k} ماله قيود من قبل\n☆")

            except:
                return m.reply(f"{k} مافي عضو بهذا اليوزر")
            m.chat.unban_member(get.user.id)
            return m.reply(f"「 {get.user.mention} 」 \n{k} ابشر الغيت حظره\n☆")

    if text == "رفع القيود" and m.reply_to_message and m.reply_to_message.from_user:
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                text = ""
                co = 0
                get = m.chat.get_member(m.reply_to_message.from_user.id)
                if get.status == ChatMemberStatus.BANNED:
                    m.chat.unban_member(get.user.id)
                    text += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    c.restrict_chat_member(
                        m.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    text += "تقييد\n"
                    co += 1
                if r.get(f"{get.user.id}:mute:{m.chat.id}{Dev_Zaid}"):
                    r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_Zaid}")
                    r.srem(f"{m.chat.id}:listMUTE:{Dev_Zaid}", get.user.id)
                    text += "كتم\n"
                    co += 1
                if co > 0:
                    return m.reply(f"رفعت القيود التالية:\n{text}\n☆")
                else:
                    return m.reply(f"「 {get.user.mention} 」\n{k} ماله قيود من قبل\n☆")
            except:
                return m.reply(f"{k} العضو مو بالمجموعة")

    if text == "كشف البوتات":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            text = "بوتات المجموعة:\n\n"
            cc = 1
            for mm in m.chat.get_members(filter=ChatMembersFilter.BOTS):
                if co == 100:
                    break
                text += f"{cc}) {mm.user.mention}"
                if mm.status == ChatMemberStatus.ADMINISTRATOR:
                    text += "👑"
                text += "\n"
                cc += 1
                co += 1
            text += "☆"
            if co == 0:
                return m.reply(f"{k} مافيه بوتات")
            else:
                return m.reply(text)

    if text == "مين ضافني":
        get = m.chat.get_member(m.from_user.id).invited_by
        if not get:
            return m.reply(f"{k} محد ضافك")
        else:
            return m.reply(get.mention)

    if text == "بايو عشوائي":
        return m.reply(f"{k} تحت الصيانة")

    if text == "مسح" and m.reply_to_message:
        if admin_pls(m.from_user.id, m.chat.id):
            m.reply_to_message.delete()
            m.delete()
        else:
            m.delete()

    if (
        text.startswith("مسح ")
        and len(text.split()) == 2
        and re.findall("[0-9]+", text)
    ):
        count = int(re.findall("[0-9]+", text)[0])
        if not admin_pls(m.from_user.id, m.chat.id):
            return m.delete()
        else:
            if count > 400:
                return m.reply(f"{k} اختار من 1 الى 400")
            else:
                for msg in range(m.id, m.id - count, -1):
                    try:
                        c.delete_messages(m.chat.id, msg)
                    except:
                        pass

    if text.startswith("تنزيل مشرف "):
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            if not '@' in text and not re.findall('[0-9]+', text):
              return
            user = text.split()[-1]
            if user.startswith('@'):
               try:
                  get_user = c.get_users(user.lstrip('@'))
                  id = get_user.id
                  mention = f'[{get_user.first_name}](tg://user?id={id})'
               except:
                  return m.reply(f'{k} مافيه عضو بهذا اليوزر')
            else:
               try:
                  get_user = c.get_chat(int(user))
                  id = get_user.id
                  mention = f'[{get_user.first_name}](tg://user?id={id})'
               except:
                  return m.reply(f'{k} مافيه عضو بهذا الآيدي')
            try:
                c.promote_chat_member(
                    m.chat.id,
                    id,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_promote_members=False,
                        can_pin_messages=False,
                        can_change_info=False,
                        can_invite_users=False,
                    ),
                )
                return m.reply(
                    f"「 {mention} 」\n{k} نزلته من الاشراف"
                )
            except:
                return m.reply(
                    f"「 {mention} 」\n{k} مو انا الي رفعته او ماعندي صلاحيات"
                )

    if text == "تنزيل مشرف" and m.reply_to_message and m.reply_to_message.from_user:
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            try:
                c.promote_chat_member(
                    m.chat.id,
                    m.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_promote_members=False,
                        can_pin_messages=False,
                        can_change_info=False,
                        can_invite_users=False,
                    ),
                )
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」\n{k} نزلته من الاشراف"
                )
            except:
                return m.reply(
                    f"「 {m.reply_to_message.from_user.mention} 」\n{k} مو انا الي رفعته او ماعندي صلاحيات"
                )

    if text.startswith("رفع مشرف "):
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            if not '@' in text and not re.findall('[0-9]+', text):
              return
            user = text.split()[-1]
            if user.startswith('@'):
               try:
                  get_user = c.get_users(user.lstrip('@'))
                  target_id = get_user.id
               except:
                  return m.reply(f'{k} مافيه عضو بهذا اليوزر')
            else:
               try:
                  get_user = c.get_chat(int(user))
                  target_id = get_user.id
               except:
                  return m.reply(f'{k} مافيه عضو بهذا الآيدي')
            get = m.chat.get_member(c.me.id)
            priv = get.privileges
            if (
                not priv.can_manage_chat
                or not priv.can_delete_messages
                or not priv.can_restrict_members
                or not priv.can_pin_messages
                or not priv.can_invite_users
                or not priv.can_change_info
                or not priv.can_promote_members
            ):
                return m.reply("هات كل الصلاحيات بعدين سولف")
            else:
                import json as _json
                promo_data = _json.dumps({"del":0,"pin":0,"ban":0,"inv":1,"vid":1,"info":0,"promo":0})
                promo_key = f"promo:{m.from_user.id}:{m.chat.id}"
                r.set(promo_key, promo_data, ex=600)
                r.set(f"promo_target:{m.from_user.id}:{m.chat.id}", target_id, ex=600)
                return m.reply(
                    f"⇜ اختر صلاحيات المشرف:\n\n✅ = مفعّل  |  ❌ = معطّل\nاضغط على الصلاحية لتغييرها",
                    reply_markup=_build_promote_keyboard(m.from_user.id, m.chat.id, _json.loads(promo_data))
                )

    if text == "رفع مشرف" and m.reply_to_message and m.reply_to_message.from_user:
        if not owner_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            get = m.chat.get_member(c.me.id)
            priv = get.privileges
            if (
                not priv.can_manage_chat
                or not priv.can_delete_messages
                or not priv.can_restrict_members
                or not priv.can_pin_messages
                or not priv.can_invite_users
                or not priv.can_change_info
                or not priv.can_promote_members
            ):
                return m.reply("هات كل الصلاحيات بعدين سولف")
            else:
                import json as _json
                promo_data = _json.dumps({"del":0,"pin":0,"ban":0,"inv":1,"vid":1,"info":0,"promo":0})
                promo_key = f"promo:{m.from_user.id}:{m.chat.id}"
                r.set(promo_key, promo_data, ex=600)
                r.set(f"promo_target:{m.from_user.id}:{m.chat.id}", m.reply_to_message.from_user.id, ex=600)
                return m.reply(
                    f"⇜ اختر صلاحيات المشرف:\n\n✅ = مفعّل  |  ❌ = معطّل\nاضغط على الصلاحية لتغييرها",
                    reply_markup=_build_promote_keyboard(m.from_user.id, m.chat.id, _json.loads(promo_data))
                )

    if text == "مسح قائمة التثبيت":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            c.unpin_all_chat_messages(m.chat.id)
            return m.reply(f"{k} ابشر مسحت قائمة التثبيت")

    if (
        text == "الاوامر"
        or text.lower() == "/commands"
        or text.lower() == f"/commands@{botUsername.lower()}"
    ):
        if admin_pls(m.from_user.id, m.chat.id):
            channel = (
                r.get(f"{Dev_Zaid}:BotChannel")
                if r.get(f"{Dev_Zaid}:BotChannel")
                else "eeeCASH"
            )
            return m.reply(
                f"{k} اهلين فيك باوامر البوت\n\nللاستفسار - @W_WT1",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "م1", callback_data=f"commands1:{m.from_user.id}"
                            ),
                            InlineKeyboardButton(
                                "م2", callback_data=f"commands2:{m.from_user.id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "م3", callback_data=f"commands3:{m.from_user.id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                            ),
                            InlineKeyboardButton(
                                "التسليه", callback_data=f"commands5:{m.from_user.id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "البنك", callback_data=f"commands7:{m.from_user.id}"
                            ),
                            InlineKeyboardButton(
                                "زواج", callback_data=f"commands8:{m.from_user.id}"
                            ),
                        ],
                    ]
                ),
            )
        else:
            return m.reply(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")

    if text == "الالعاب":
        return m.reply(
            """
☤ تفعيل الالعاب
☤ تعطيل الالعاب
    ╼╾
✽ جمل
✽ كلمات
✽ اغاني
✽ دين
✽ عربي
✽ اكمل
✽ صور
✽ كت تويت
✽ مؤقت
✽ اعلام
✽ معاني
✽ تخمين
✽ احكام
✽ ارقام
✽ احسب
✽ خواتم
✽ انقليزي
✽ ترتيب
✽ انمي
✽ تركيب
✽ تفكيك
✽ عواصم
✽ روليت
✽ سيارات
✽ ايموجي
✽ حجره
✽ تشفير
✽ كره قدم
✽ ديمون
✽ القلاع
✽ الغزاة
✽ النوادي
✽ اكس او
✽ لغز
╼╾
❖ فلوسي ↼ عشان تشوف فلوسك
❖ بيع فلوسي + العدد ↼ للأستبدال
            """
        )



@Client.on_callback_query(group=1)
def CallbackQueryHandler(c, m):
    if not getattr(m, 'from_user', None): return
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "eeeCASH"
    )
    Thread(target=CallbackQueryResponse, args=(c, m, channel)).start()


def CallbackQueryResponse(c, m, channel):
    if not getattr(m, 'from_user', None): return
    k = r.get(f"{Dev_Zaid}:botkey")
    if m.data == f"commands1:{m.from_user.id}":
        m.edit_message_text(
            f"""
للاستفسار - @W_WT1


❨ اوامر الرفع والتنزيل ❩

⌯ رفع ↣ ↢ تنزيل مميز
⌯ رفع ↣ ↢ تنزيل ادمن
⌯ رفع ↣ ↢ تنزيل مدير
⌯ رفع ↣ ↢ تنزيل مالك
⌯ رفع ↣ ↢ تنزيل مالك اساسي
⌯ رفع ↣ ↢ تنزيل منشئ
⌯ رفع ↣ ↢ تنزيل منشئ اساسي
⌯ رفع ↣ ↢ تنزيل مطور
⌯ رفع ↣ ↢ تنزيل مشرف
⌯ تنزيل الكل  ↢ بالرد  ↢ لتنزيل الشخص من جميع رتبه
⌯ مسح الكل  ↢ بدون رد  ↢ لتنزيل كل رتب المجموعة

❨ اوامر المسح ❩

⌯ مسح المالكيين
⌯ مسح المدراء
⌯ مسح الادمنيه
⌯ مسح المميزين
⌯ مسح المحظورين
⌯ مسح المكتومين
⌯ مسح قائمة المنع
⌯ مسح رتبه
⌯ مسح الرتب
⌯ مسح الرتب الوهميه
⌯ مسح الردود
⌯ مسح الاوامر
⌯ مسح + العدد
⌯ مسح بالرد
⌯ مسح الترحيب
⌯ مسح قائمة التثبيت
⌯ مسح التعديل

❨ اوامر الطرد الحظر الكتم ❩

⌯ حظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ طرد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ كتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ تقيد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الحظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الكتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء التقييد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ رفع القيود ↢ لحذف الكتم,الحظر,التقييد
⌯ برنت ↢ ❨ بالرد،بالمعرف،بالايدي ❩ لمعرفة قيود العضو
⌯ منع الكلمة
⌯ منع بالرد على قيف او ستيكر
⌯ الغاء منع الكلمة
⌯ طرد البوتات
⌯ كشف البوتات

❨ اوامر النطق ❩

⌯ انطقي + الكلمة
⌯ وش يقول؟ + بالرد على فويس لترجمه المحتوى

❨ اوامر اخرى ❩

⌯ الرابط
⌯ معلومات الرابط
⌯ انشاء رابط
⌯ بايو
⌯ بايو عشوائي
⌯ ايدي
⌯ الانشاء
⌯ مجموعاتي
⌯ ابلاغ
⌯ نقل ملكية
⌯ صوره
⌯ افتاري
⌯ افتار + باليوزر او الرد
⌯ مين ضافني؟
⌯ شازام، قرآن، سورة + اسم السورة
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("م1 ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands2:{m.from_user.id}":
        m.edit_message_text(
            f"""
للاستفسار - @W_WT1


❨ اوامر الوضع ❩

⌯ وضع ترحيب
⌯ وضع قوانين
⌯ تغيير رتبه
⌯ تغيير امر
⌯ تغيير كليشة المالك
⌯ تغيير المالك


❨ اوامر رؤية الاعدادات ❩

⌯ المطورين
⌯ المنشئين الاساسيين
⌯ المالكيين الاساسيين
⌯ المالكيين
⌯ الادمنيه
⌯ المدراء
⌯ المشرفين
⌯ المميزين
⌯ القوانين
⌯ قائمه المنع
⌯ المكتومين
⌯ المطور
⌯ معلوماتي
⌯ الاعدادت
⌯ المجموعه
⌯ الساعه
⌯ التاريخ
⌯ صلاحياتي
⌯ لقبي
⌯ صلاحياته + بالرد
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton("م2 ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands3:{m.from_user.id}":
        m.edit_message_text(
            f"""
للاستفسار - @W_WT1


❨ اوامر الردود ❩

⌯ الردود ↢ تشوف كل الردود المضافه
⌯ الردود المتعدده ↢ تشوف كل الردود المتعدده المضافه
⌯ اضف رد ↢ عشان تضيف رد
⌯ اضف رد متعدد ↢ عشان تضيف أكثر من رد
⌯ اضف رد متعدد ↢ خاص بالاعضاء
⌯ مسح رد ↢ عشان تمسح الرد
⌯ مسح رد متعدد ↢ عشان تمسح رد متعدد
⌯ مسح ردي ↢ عشان تمسح ردك اذا كان بردود الأعضاء
⌯ مسح الردود ↢ تمسح كل الردود
⌯ مسح الردود المتعدده ↢ عشان تمسح كل الردود المتعدده
⌯ الرد + كلمة الرد
-

❨ اوامر القفل والفتح بالمسح ❩

⌯ قفل ↣ ↢ فتح  التعديل
⌯ قفل ↣ ↢ فتح  الفويسات
⌯ قفل ↣ ↢ فتح  الفيديو
⌯ قفل ↣ ↢ فتح  الـصــور
⌯ قفل ↣ ↢ فتح  الملصقات
⌯ قفل ↣ ↢ فتح  الدخول
⌯ قفل ↣ ↢ فتح  الفارسيه
⌯ قفل ↣ ↢ فتح  الملفات
⌯ قفل ↣ ↢ فتح  المتحركات
⌯ قفل ↣ ↢ فتح  تعديل الميديا
⌯ قفل ↣ ↢ فتح  تعديل الميديا بالتقييد
⌯ قفل ↣ ↢ فتح  الدردشه
⌯ قفل ↣ ↢ فتح  الروابط
⌯ قفل ↣ ↢ فتح  الهشتاق
⌯ قفل ↣ ↢ فتح  البوتات
⌯ قفل ↣ ↢ فتح  اليوزرات
⌯ قفل ↣ ↢ فتح  الاشعارات
⌯ قفل ↣ ↢ فتح  الكلام الكثير
⌯ قفل ↣ ↢ فتح  التكرار بالكتم
⌯ وضع التكرار + العدد
⌯ قفل ↣ ↢ فتح  التوجيه
⌯ قفل ↣ ↢ فتح  الانلاين
⌯ قفل ↣ ↢ فتح  الجهات
⌯ قفل ↣ ↢ فتح  الــكـــل
⌯ قفل ↣ ↢ فتح  السب
⌯ قفل ↣ ↢ فتح  الاضافه
⌯ قفل ↣ ↢ فتح  الصوت
⌯ قفل ↣ ↢ فتح  القنوات
⌯ قفل ↣ ↢ فتح الايراني
⌯ قفل ↣ ↢ فتح الإباحي

❨ اوامر التفعيل والتعطيل ❩

⌯ تفعيل ↣ ↢ تعطيل الترحيب
⌯ تفعيل ↣ ↢ تعطيل الترحيب بالصورة
⌯ تفعيل ↣ ↢ تعطيل الردود
⌯ تفعيل ↣ ↢ تعطيل ردود الاعضاء
⌯ تفعيل ↣ ↢ تعطيل الايدي
⌯ تفعيل ↣ ↢ تعطيل الرابط
⌯ تفعيل ↣ ↢ تعطيل الرابط العادي
⌯ تفعيل ↣ ↢ تعطيل اطردني
⌯ تفعيل ↣ ↢ تعطيل الحماية
⌯ تفعيل ↣ ↢ تعطيل حماية التلاعب
⌯ تفعيل ↣ ↢ تعطيل الوضع الليلي
⌯ تفعيل ↣ ↢ تعطيل المنشن
⌯ تفعيل ↣ ↢ تعطيل التحقق
⌯ تفعيل ↣ ↢ تعطيل ردود المطور
⌯ تفعيل ↣ ↢ تعطيل التحذير
⌯ تفعيل ↣ ↢ تعطيل البايو
⌯ تفعيل ↣ ↢ تعطيل انطقي
⌯ تفعيل ↣ ↢ تعطيل شازام

❨ اوامر التنظيف والمسح ❩

⌯ مسح [العدد] ↢ لمسح الميديا في الجروب
⌯ مسح الكل [العدد] ↢ لمسح الرسائل بالكامل
⌯ مسح التعديل ↢ لمسح الرسائل المعدلة
⌯ تفعيل ↣ ↢ تعطيل المسح ↢ للمسح التلقائي
⌯ وقت المسح [المدة] ↢ لتغيير مدة المسح (مثال: وقت المسح 10 دقائق)
⌯ نوع المسح [الميديا/الكل] ↢ لتحديد نوع المسح التلقائي
⌯ تفعيل ↣ ↢ تعطيل التنظيف
⌯ وضع وقت التنظيف + [العدد بالثواني]
⌯ وقت التنظيف
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("م3 ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands4:{m.from_user.id}":
        m.edit_message_text(
            """
☤ تفعيل الالعاب
☤ تعطيل الالعاب
    ╼╾
✽ جمل
✽ كلمات
✽ اغاني
✽ دين
✽ عربي
✽ اكمل
✽ صور
✽ كت تويت
✽ مؤقت
✽ اعلام
✽ معاني
✽ تخمين
✽ احكام
✽ ارقام
✽ احسب
✽ خواتم
✽ انقليزي
✽ ترتيب
✽ انمي
✽ تركيب
✽ تفكيك
✽ عواصم
✽ روليت
✽ سيارات
✽ ايموجي
✽ حجره
✽ تشفير
✽ كره قدم
✽ ديمون
✽ القلاع
✽ الغزاة
✽ النوادي
✽ اكس او
✽ لغز
╼╾
❖ فلوسي ↼ عشان تشوف فلوسك
❖ بيع فلوسي + العدد ↼ للأستبدال
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("الالعاب ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands5:{m.from_user.id}":
        m.edit_message_text(
            f"""
للاستفسار - @W_WT1

🍰 ⌯ رفع ↣ ↢ تنزيل كيكه
🍯 ⌯ رفع ↣ ↢ تنزيل عسل
💩 ⌯ رفع ↣ ↢ تنزيل زق
🦓 ⌯ رفع ↣ ↢ تنزيل حمار
🐄 ⌯ رفع ↣ ↢ تنزيل بقره
🐩 ⌯ رفع ↣ ↢ تنزيل كلب
🐒 ⌯ رفع ↣ ↢ تنزيل قرد
🐐 ⌯ رفع ↣ ↢ تنزيل تيس
🐂 ⌯ رفع ↣ ↢ تنزيل ثور
🏅 ⌯ رفع ↣ ↢ تنزيل هكر
🐓 ⌯ رفع ↣ ↢ تنزيل دجاجه
🧱 ⌯ رفع ↣ ↢ تنزيل ملكه
🔫 ⌯ رفع ↣ ↢ تنزيل صياد
🐏 ⌯ رفع ↣ ↢ تنزيل خاروف
❤️ ⌯ رفع لقلبي ↣ ↢ تنزيل من قلبي

⌯ قائمة الكيك
⌯ قائمة العسل
⌯ قائمة الزق
⌯ قائمة الحمير
⌯ قائمة البقر
⌯ قائمة الكلاب
⌯ قائمة القرود
⌯ قائمة التيس
⌯ قائمة الثور
⌯ قائمة الهكر
⌯ قائمة الدجاج
⌯ قائمة الهطوف
⌯ قائمة الصيادين
⌯ قائمة الخرفان
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton("التسليه ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands6:{m.from_user.id}":
        m.edit_message_text(
            """
⚘ اليـوتيوب

تفعيل اليوتيوب
تعطيل اليوتيوب

❋ البـحث عن اغنية ↓

بحث اسم الاغنية

يوت اسم الاغنية
⚘ الساوند كلاود

تفعيل الساوند
تعطيل الساوند

❋ البـحث عن اغنية ↓

رابط الاغنية أو ساوند + اسم الاغنية


⚘ التيك توك

تفعيل التيك
تعطيل للتيك

❋ للتحميل من التيك ↓

تيك ورابط المقطع
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("اليوتيوب ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands7:{m.from_user.id}":
        m.edit_message_text(
            """
✜ اوامر البنك

⌯ انشاء حساب بنكي  ↢ تسوي حساب وتقدر تحول فلوس مع مزايا ثانيه

⌯ مسح حساب بنكي  ↢ تلغي حسابك البنكي

⌯ تحويل ↢ تطلب رقم حساب الشخص وتحول له فلوس

⌯ حسابي  ↢ يطلع لك رقم حسابك عشان تعطيه للشخص اللي بيحول لك

⌯ فلوسي ↢ يعلمك كم فلوسك

⌯ راتب ↢ يعطيك راتبك كل ٥ دقيقة

⌯ بخشيش ↢ يعطيك بخشيش كل ٥ دقايق

⌯ زرف ↢ تزرف فلوس اشخاص كل ٥ دقايق

⌯ كنز ↢ يعطيك كنز كل ١٠ دقايق

⌯ استثمار ↢ تستثمر بالمبلغ اللي تبيه مع نسبة ربح مضمونه من ١٪؜ الى ١٥٪؜ ( او استثمار فلوسي )

⌯ حظ ↢ تلعبها بأي مبلغ ياتدبله ياتخسره انت وحظك ( او حظ فلوسي )

⌯ عجله ↢ تلعب عجله الحظ ولو تشابهو ال ٣ ايموجيات تكسب من ١٠٠ الف لحد ٣٠٠ الف انت وحظك

⌯ توب الفلوس ↢ يطلع توب اكثر ناس معهم فلوس بكل القروبات

⌯ توب الحراميه ↢ يطلع لك اكثر ناس زرفوا
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("البنك ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{m.from_user.id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if m.data == f"commands8:{m.from_user.id}":
        m.edit_message_text(
            """
✜ اوامر الزواج

⌯ زواج  ↢ تكتبه بالرد على رسالة شخص مع المهر ويزوجك

⌯ زواجي  ↢ يطلع وثيقة زواجك اذا متزوج

⌯ طلاق ↢ يطلقك اذا متزوج

⌯ خلع  ↢ يخلع زوجك ويرجع له المهر

⌯ زواجات ↢ يطلع اغلى الزواجات بالقروب
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{m.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{m.from_user.id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{m.from_user.id}"
                        ),
                        InlineKeyboardButton("زواج ‣", callback_data="None"),
                    ],
                ]
            ),
        )
        return

    if m.data == "delAdminMSG":
        if str(m.from_user.id) in m.message.text.html:
            return m.message.delete()

    if m.data == f"yes:{m.from_user.id}":
        try:
            c.restrict_chat_member(
                m.message.chat.id,
                m.from_user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
        except:
            return False
        m.edit_message_text(
            f"""
{k} تم التحقق منك وطلعت مو زومبي
{k} الحين تقدر تسولف بالقروب
☆
""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            ),
        )

    if m.data == f"no:{m.from_user.id}":
        return m.edit_message_text(
            f"""
{k} للأسف طلعت زومبي 🧟‍♀️
{k} مالك غير تنطر حد من المشرفين يجي يتوسطلك
☆
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "رفع التقييد والسماح",
                            callback_data=f"yesVER:{m.from_user.id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "طرد", callback_data=f"noVER:{m.from_user.id}"
                        )
                    ],
                ]
            ),
        )

    if m.data.startswith("yesVER"):
        user_id = int(m.data.split(":")[1])
        if not admin_pls(m.from_user.id, m.message.chat.id):
            return m.answer(f"{k} هذا الزر يخص ( الادمن وفوق ) بس", show_alert=True)
        else:
            m.edit_message_text(f"{k} توسطلك واحد من الادمن ورفعت عنك القيود")
            try:
                c.restrict_chat_member(
                    m.message.chat.id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_pin_messages=True,
                    ),
                )
            except:
                return False

    if m.data.startswith("noVER"):
        user_id = int(m.data.split(":")[1])
        if not admin_pls(m.from_user.id, m.message.chat.id):
            return m.answer(f"{k} هذا الزر يخص ( الادمن وفوق ) بس", show_alert=True)
        else:
            m.edit_message_text(f"{k} انقلع برا القروب يلا")
            try:
                m.message.chat.ban_member(user_id)
                m.message.chat.unban_member(user_id)
            except:
                pass

    if m.data == "yes:del:bank":
        if not devp_pls(m.from_user.id, m.message.chat.id):
            return m.answer("تعجبني ثقتك")
        else:
            m.edit_message_text("ابشر صفرت البنك")
            keys = r.keys("*:Floos")
            for a in keys:
                r.delete(a)
            for a in r.keys("*:BankWait"):
                r.delete(a)
            for a in r.keys("*:BankWaitB5"):
                r.delete(a)
            for a in r.keys("*:BankWaitZRF"):
                r.delete(a)
            for a in r.keys("*:BankWaitEST"):
                r.delete(a)
            for a in r.keys("*:BankWaitHZ"):
                r.delete(a)
            for a in r.keys("*:BankWait3JL"):
                r.delete(a)
            for a in r.keys("*:Zrf"):
                r.delete(a)
            r.delete("BankTop")
            r.delete("BankTopZRF")
            return True

    if m.data == "no:del:bank":
        if not devp_pls(m.from_user.id, m.message.chat.id):
            return m.answer("تعجبني ثقتك")
        else:
            m.message.delete()

    if m.data == f"topfloos:{m.from_user.id}":
        if not r.smembers("BankList"):
            return m.answer(f"{k} مافيه حسابات بالبنك", show_alert=True)
        else:
            rep = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("‣ 💸", callback_data="None"),
                        InlineKeyboardButton(
                            "توب الحرامية 💰", callback_data=f"topzrf:{m.from_user.id}"
                        ),
                    ],
                    [InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")],
                ]
            )
            if r.get("BankTop"):
                text = r.get("BankTop")
                if not r.get(f"{m.from_user.id}:Floos"):
                    floos = 0
                else:
                    floos = int(r.get(f"{m.from_user.id}:Floos"))
                get = r.ttl("BankTop")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos:,} 💸 l {m.from_user.first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                return m.edit_message_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )
            else:
                users = []
                ccc = 0
                for user in r.smembers("BankList"):
                    ccc += 1
                    id = int(user)
                    if r.get(f"{id}:bankName"):
                        name = r.get(f"{id}:bankName")[:10]
                    else:
                        try:
                            name = c.get_chat(id).first_name
                            r.set(f"{id}:bankName", name)
                        except:
                            name = "INVALID_NAME"
                            r.set(f"{id}:bankName", name)
                    if not r.get(f"{id}:Floos"):
                        floos = 0
                    else:
                        floos = int(r.get(f"{id}:Floos"))
                    users.append({"name": name, "money": floos})
                top = get_top(users)
                text = "توب 20 اغنى اشخاص:\n\n"
                count = 0
                for user in top:
                    count += 1
                    if count == 21:
                        break
                    emoji = get_emoji_bank(count)
                    floos = user["money"]
                    name = user["name"]
                    text += f'**{emoji}{floos:,}** 💸 l {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
                r.set("BankTop", text, ex=300)
                if not r.get(f"{m.from_user.id}:Floos"):
                    floos_from_user = 0
                else:
                    floos_from_user = int(r.get(f"{m.from_user.id}:Floos"))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos_from_user:,} 💸 l {m.from_user.first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                get = r.ttl("BankTop")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                m.edit_message_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )

    if m.data == f"topzrf:{m.from_user.id}":
        if not r.smembers("BankList"):
            return m.answer(f"{k} مافيه حسابات بالبنك", show_alert=True)
        else:
            rep = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "توب الفلوس 💸", callback_data=f"topfloos:{m.from_user.id}"
                        ),
                        InlineKeyboardButton("‣ 💰", callback_data="None"),
                    ],
                    [InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")],
                ]
            )
            if r.get("BankTopZRF"):
                text = r.get("BankTopZRF")
                if not r.get(f"{m.from_user.id}:Zrf"):
                    zrf = 0
                else:
                    zrf = int(r.get(f"{m.from_user.id}:Zrf"))
                get = r.ttl("BankTopZRF")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {zrf:,} 💰 l {m.from_user.first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                return m.edit_message_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )
            else:
                users = []
                ccc = 0
                for user in r.smembers("BankList"):
                    ccc += 1
                    id = int(user)
                    if r.get(f"{id}:bankName"):
                        name = r.get(f"{id}:bankName")[:10]
                    else:
                        try:
                            name = c.get_chat(id).first_name
                            r.set(f"{id}:bankName", name)
                        except:
                            name = "INVALID_NAME"
                            r.set(f"{id}:bankName", name)
                    if not r.get(f"{id}:Zrf"):
                        pass
                    else:
                        zrf = int(r.get(f"{id}:Zrf"))
                        users.append({"name": name, "money": zrf})
                top = get_top(users)
                text = "توب 20 اكثر الحراميه زرفًا:\n\n"
                count = 0
                for user in top:
                    count += 1
                    if count == 21:
                        break
                    emoji = get_emoji_bank(count)
                    floos = user["money"]
                    name = user["name"]
                    text += f'**{emoji}{floos}** 💰 l {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
                r.set("BankTopZRF", text, ex=300)
                if not r.get(f"{m.from_user.id}:Zrf"):
                    floos_from_user = 0
                else:
                    floos_from_user = int(r.get(f"{m.from_user.id}:Zrf"))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos_from_user} 💰 l {m.from_user.first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                get = r.ttl("BankTopZRF")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                m.edit_message_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )

    """
   if m.data == f'toplast:{m.from_user.id}':
     if not r.get(f'BankTopLast') and not r.get(f'BankTopLastZrf'):
       return m.answer(f'{k} مافي توب اسبوع الي فات',show_alert=True)
     else:
       text = 'توب أوائل الأسبوع الي راح:\n'
       text += r.get(f'BankTopLast')
       text += '\n\nتوب حرامية الاسبوع اللي راح:\n'
       text += r.get(f'BankTopLastZrf')
       text += '\n༄'
       rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')]]
       )
       m.edit_message_text(text, disable_web_page_preview=True,reply_markup=rep)
   """

    name = r.get(f"{Dev_Zaid}:BotName") if r.get(f"{Dev_Zaid}:BotName") else "اتاك"
    if m.data == f"RPS:rock++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "scissors":
            if r.get(f"{m.from_user.id}:Floos"):
                get = int(r.get(f"{m.from_user.id}:Floos"))
                r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 🪨
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ 🏆 {m.from_user.first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 🪨
أنا: 📃

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 🪨
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

    if m.data == f"gowner+{m.from_user.id}":
        if not gowner_pls(m.from_user.id, m.message.chat.id):
            m.asnwer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{m.message.chat.id}", command, 0)
            return m.edit_message_text(
                f"- تم تعيين الامر ( {command} ) للمالك الاساسي وفوق فقط"
            )

    if m.data == f"owner+{m.from_user.id}":
        if not gowner_pls(m.from_user.id, m.message.chat.id):
            m.asnwer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{m.message.chat.id}", command, 1)
            return m.edit_message_text(
                f"- تم تعيين الامر ( {command} ) للمالك وفوق فقط"
            )

    if m.data == f"mod+{m.from_user.id}":
        if not gowner_pls(m.from_user.id, m.message.chat.id):
            m.asnwer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{m.message.chat.id}", command, 2)
            return m.edit_message_text(
                f"- تم تعيين الامر ( {command} ) للمدير وفوق فقط"
            )

    if m.data == f"admin+{m.from_user.id}":
        if not gowner_pls(m.from_user.id, m.message.chat.id):
            m.asnwer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{m.message.chat.id}", command, 3)
            return m.edit_message_text(
                f"- تم تعيين الامر ( {command} ) للادمن وفوق فقط"
            )

    if m.data == f"pre+{m.from_user.id}":
        if not gowner_pls(m.from_user.id, m.message.chat.id):
            m.asnwer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{m.message.chat.id}", command, 4)
            return m.edit_message_text(
                f"- تم تعيين الامر ( {command} ) للمميز وفوق فقط"
            )

    if m.data == f"RPS:paper++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "rock":
            if r.get(f"{m.from_user.id}:Floos"):
                get = int(r.get(f"{m.from_user.id}:Floos"))
                r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 📃
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ 🏆 {m.from_user.first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 📃
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: 📃
أنا: 📃

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

    if m.data == f"RPS:scissors++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "paper":
            if r.get(f"{m.from_user.id}:Floos"):
                get = int(r.get(f"{m.from_user.id}:Floos"))
                r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: ✂️
أنا: 📃

النتيجة: ⁪⁬⁪⁬ 🏆 {m.from_user.first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: ✂️
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"https://t.me/{channel}")]]
            )
            m.edit_message_text(
                f"""
أنت: ✂️
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )


@Client.on_callback_query(filters.regex(r"^prm_"))
def promote_callback(c, m):
    if not getattr(m, 'from_user', None): return
    Thread(target=promote_callback_thread, args=(c, m)).start()

def promote_callback_thread(c, m):
    k = r.get(f"{Dev_Zaid}:botkey")
    data = m.data.split("_")
    action = data[1]
    user_id = int(data[2])
    chat_id = int(data[3])
    
    if m.from_user.id != user_id:
        return m.answer("هذا الأمر لا يخصك", show_alert=True)
        
    promo_key = f"promo:{user_id}:{chat_id}"
    promo_data_str = r.get(promo_key)
    if not promo_data_str:
        return m.answer("انتهت الجلسة، الرجاء إعادة الأمر", show_alert=True)
        
    import json
    from pyrogram.errors import MessageNotModified
    perms = json.loads(promo_data_str)
    
    if action == "cancel":
        r.delete(promo_key)
        r.delete(f"promo_target:{user_id}:{chat_id}")
        return m.edit_message_text(f"تم إلغاء رفع المشرف")
        
    if action == "all":
        for k_item in perms.keys():
            perms[k_item] = 1
        r.set(promo_key, json.dumps(perms), ex=600)
        try:
            return m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
        except MessageNotModified:
            return
        
    if action == "none":
        for k_item in perms.keys():
            perms[k_item] = 0
        r.set(promo_key, json.dumps(perms), ex=600)
        try:
            return m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
        except MessageNotModified:
            return
        
    if action == "done":
        target_id = r.get(f"promo_target:{user_id}:{chat_id}")
        if not target_id:
            return m.answer("حدث خطأ", show_alert=True)
        target_id = int(target_id)
        
        try:
            c.promote_chat_member(
                chat_id,
                target_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=bool(perms["del"]),
                    can_manage_video_chats=bool(perms["vid"]),
                    can_restrict_members=bool(perms["ban"]),
                    can_promote_members=bool(perms["promo"]),
                    can_change_info=bool(perms["info"]),
                    can_invite_users=bool(perms["inv"]),
                    can_pin_messages=bool(perms["pin"]),
                ),
            )
            get = m.message.chat.get_member(target_id)
            r.set(f"{chat_id}:rankADMIN:{get.user.id}{Dev_Zaid}", 1)
            r.sadd(f"{chat_id}:listADMIN:{Dev_Zaid}", get.user.id)
            r.delete(promo_key)
            r.delete(f"promo_target:{user_id}:{chat_id}")
            m.edit_message_text(f"الحلو 「 {get.user.mention} 」\n{k} رفعته مشرف بالصلاحيات المحددة")
        except Exception as e:
            m.edit_message_text(f"{k} ما قدرت ارفعه، تأكد انه عضو في المجموعة")
        return
        
    # Toggle individual
    if action in perms:
        perms[action] = 1 if perms[action] == 0 else 0
        r.set(promo_key, json.dumps(perms), ex=600)
        try:
            m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
        except MessageNotModified:
            pass
