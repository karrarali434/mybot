import os
import requests
from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from config import owner_id, IS_FACTORY

try:
    from helpers.bot_manager import clone_bot, start_bot, stop_bot, remove_bot, get_all_bots, get_bot, is_process_running, update_bot_status, calculate_remaining_time
except ImportError:
    pass

AWAITING_TOKEN = {}
AWAITING_DURATION = {}

def awaiting_token_filter(_, __, message: Message):
    return bool(AWAITING_TOKEN.get(message.from_user.id))

awaiting_token = filters.create(awaiting_token_filter)

def is_factory_filter(_, __, ___):
    return IS_FACTORY

is_factory = filters.create(is_factory_filter)
factory_owners = [owner_id, 6791079130]

@Client.on_message(filters.command("start") & filters.private & is_factory, group=-1)
async def factory_start_all(client: Client, message: Message):
    if message.from_user and message.from_user.id in factory_owners:
        text = "✨ أهلاً بك في مصنع بوتات الحماية الخاص بك!\n\nيمكنك من خلال هذه اللوحة إدارة البوتات وصنع نسخ جديدة بسهولة."
        keyboard = [
            [InlineKeyboardButton("➕ صنع بوت حماية جديد", callback_data="make_new_bot")],
            [InlineKeyboardButton("📊 البوتات المصنوعة", callback_data="bots_list")],
        ]
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        text = "عذراً، يجب عليك التواصل مع المطور @W_WT1 لكي تشترك وتصنع بوت خاص بك باشتراك شهري وبكامل حقوقك."
        await message.reply_text(text)
    raise StopPropagation

@Client.on_callback_query(filters.regex(r"^make_new_bot$") & filters.user(factory_owners) & is_factory)
async def make_new_bot_cb(client: Client, query: CallbackQuery):
    AWAITING_TOKEN[query.from_user.id] = True
    await query.message.edit_text("✨ يرجى إرسال توكن البوت الجديد الذي حصلت عليه من @BotFather الآن:\n(لإلغاء العملية أرسل /cancel)")

@Client.on_message(filters.command(["makebot", "صنع بوت"]) & filters.user(factory_owners) & is_factory)
async def makebot_cmd(client: Client, message: Message):
    AWAITING_TOKEN[message.from_user.id] = True
    await message.reply_text("✨ أهلاً بك في مصنع البوتات!\n\nيرجى إرسال توكن البوت الجديد الذي حصلت عليه من @BotFather الآن:\n(لإلغاء العملية أرسل /cancel)")

@Client.on_message(filters.command(["cancel", "الغاء", "إلغاء"]) & filters.user(factory_owners) & awaiting_token & is_factory)
async def cancel_makebot(client: Client, message: Message):
    if message.from_user.id in AWAITING_TOKEN:
        del AWAITING_TOKEN[message.from_user.id]
        await message.reply_text("تم إلغاء عملية صنع البوت.")

@Client.on_message(filters.text & filters.user(factory_owners) & awaiting_token & is_factory)
async def handle_token(client: Client, message: Message):
    token = message.text.strip()
    if token.startswith("/"):
        return # Probably another command like /cancel
        
    if ":" not in token:
        await message.reply_text("❌ توكن غير صالح. يرجى إرسال توكن صحيح أو إرسال /cancel للإلغاء.")
        return
        
    msg = await message.reply_text("⏳ جاري التحقق من التوكن وصنع البوت...")
    
    try:
        req = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
        if not req.get("ok"):
            await msg.edit_text("❌ التوكن غير صالح! يرجى التأكد منه وإرساله مجدداً.")
            return
            
        bot_info = req["result"]
        bot_id = str(bot_info["id"])
        bot_username = bot_info["username"]
        bot_name = bot_info["first_name"]
        
        main_bot_id = str(client.me.id) if client.me else str(client.id) if hasattr(client, 'id') else owner_id
        if bot_id == main_bot_id:
            await msg.edit_text("❌ لا يمكنك استخدام توكن البوت الأساسي لعمل نسخة!")
            del AWAITING_TOKEN[message.from_user.id]
            return
            
        existing_bot = get_bot(bot_id)
        if existing_bot:
            await msg.edit_text("❌ هذا البوت مصنوع مسبقاً!")
            del AWAITING_TOKEN[message.from_user.id]
            return
            
        AWAITING_DURATION[message.from_user.id] = {
            "token": token,
            "bot_id": bot_id,
            "bot_username": bot_username,
            "bot_name": bot_name
        }
        del AWAITING_TOKEN[message.from_user.id]
        
        keyboard = []
        for i in range(1, 13, 3):
            row = [
                InlineKeyboardButton(f"{i} شهر", callback_data=f"setduration_{i}"),
                InlineKeyboardButton(f"{i+1} شهر", callback_data=f"setduration_{i+1}"),
                InlineKeyboardButton(f"{i+2} شهر", callback_data=f"setduration_{i+2}"),
            ]
            keyboard.append(row)
            
        await msg.edit_text("✅ التوكن صحيح.\n\nيرجى تحديد مدة اشتراك هذا البوت:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء صنع البوت:\n`{str(e)}`")
        if message.from_user.id in AWAITING_TOKEN:
            del AWAITING_TOKEN[message.from_user.id]

@Client.on_callback_query(filters.regex(r"^setduration_(\d+)$") & filters.user(factory_owners) & is_factory)
async def set_duration_cb(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in AWAITING_DURATION:
        await query.answer("انتهت الجلسة أو غير صالحة.", show_alert=True)
        return
        
    months = int(query.matches[0].group(1))
    bot_data = AWAITING_DURATION[user_id]
    
    await query.message.edit_text("⏳ جاري تجهيز ملفات البوت وقاعدة البيانات...")
    
    from datetime import datetime
    start_date = datetime.now().isoformat()
    
    try:
        folder = clone_bot(bot_data['token'], bot_data['bot_id'], bot_data['bot_username'], user_id, start_date=start_date, duration_months=months)
        started = start_bot(bot_data['bot_id'])
        
        del AWAITING_DURATION[user_id]
        
        text = f"""
✅ **تم صنع البوت بنجاح!**

👤 **الاسم:** {bot_data['bot_name']}
🔗 **المعرف:** @{bot_data['bot_username']}
🆔 **الآيدي:** `{bot_data['bot_id']}`
⏱ **مدة الاشتراك:** {months} شهر

⚙️ تم تجهيز ملفات البوت وقاعدة البيانات الخاصة به.
🚀 حالة التشغيل: {'شغال الآن 🟢' if started else 'فشل التشغيل 🔴'}
"""
        await query.message.edit_text(text)
    except Exception as e:
        await query.message.edit_text(f"❌ حدث خطأ أثناء صنع البوت:\n`{str(e)}`")
        if user_id in AWAITING_DURATION:
            del AWAITING_DURATION[user_id]


@Client.on_message(filters.command(["bots", "البوتات المصنوعة"]) & filters.user(factory_owners) & is_factory)
async def bots_cmd(client: Client, message: Message):
    bots = get_all_bots()
    if not bots:
        await message.reply_text("لا توجد بوتات مصنوعة حالياً.")
        return
        
    keyboard = []
    for b in bots:
        status_emoji = "🟢" if b['status'] == 'running' and is_process_running(b['pid']) else "🔴"
        keyboard.append([InlineKeyboardButton(f"{status_emoji} @{b['username']}", callback_data=f"botinfo_{b['id']}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(f"📊 **البوتات المصنوعة:** {len(bots)}", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex(r"^botinfo_(\d+)$") & filters.user(factory_owners) & is_factory)
async def bot_info_cb(client: Client, query: CallbackQuery):
    bot_id = query.data.split("_")[1]
    bot = get_bot(bot_id)
    if not bot:
        await query.answer("❌ البوت غير موجود!", show_alert=True)
        return
        
    is_running = is_process_running(bot['pid'])
    if bot['status'] == 'running' and not is_running:
        update_bot_status(bot_id, 'stopped', None)
        bot['status'] = 'stopped'
        
    status_text = "يعمل 🟢" if is_running else "متوقف 🔴"
    
    remaining_time, end_date = calculate_remaining_time(bot.get('start_date'), bot.get('duration_months'))
    start_date_display = bot.get('start_date', '').split('T')[0] if bot.get('start_date') else "غير محدد"
    
    text = f"""
🤖 **معلومات البوت:**
- المعرف: @{bot['username']}
- الآيدي: `{bot['id']}`
- الحالة: {status_text}
- تاريخ الإنشاء: `{start_date_display}`
- مدة الاشتراك: `{bot.get('duration_months', 'غير محدد')} شهر`
- تاريخ الانتهاء: `{end_date}`
- الوقت المتبقي: `{remaining_time}`
"""
    keyboard = []
    if is_running:
        keyboard.append([InlineKeyboardButton("⏸ إيقاف", callback_data=f"botstop_{bot_id}"), InlineKeyboardButton("🔄 إعادة تشغيل", callback_data=f"botrestart_{bot_id}")])
    else:
        keyboard.append([InlineKeyboardButton("▶️ تشغيل", callback_data=f"botstart_{bot_id}")])
        
    keyboard.append([InlineKeyboardButton("🗑 حذف البوت نهائياً", callback_data=f"botdelete_{bot_id}")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="bots_list")])
    
    try:
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    except MessageNotModified:
        pass


@Client.on_callback_query(filters.regex(r"^botstop_(\d+)$") & filters.user(factory_owners) & is_factory)
async def bot_stop_cb(client: Client, query: CallbackQuery):
    bot_id = query.data.split("_")[1]
    stop_bot(bot_id)
    await query.answer("تم إيقاف البوت ⏸", show_alert=True)
    await bot_info_cb(client, query)


@Client.on_callback_query(filters.regex(r"^botstart_(\d+)$") & filters.user(factory_owners) & is_factory)
async def bot_start_cb(client: Client, query: CallbackQuery):
    bot_id = query.data.split("_")[1]
    started = start_bot(bot_id)
    if started:
        await query.answer("تم تشغيل البوت ▶️", show_alert=True)
    else:
        await query.answer("❌ فشل تشغيل البوت!", show_alert=True)
    await bot_info_cb(client, query)

@Client.on_callback_query(filters.regex(r"^botrestart_(\d+)$") & filters.user(factory_owners) & is_factory)
async def bot_restart_cb(client: Client, query: CallbackQuery):
    bot_id = query.data.split("_")[1]
    stop_bot(bot_id)
    start_bot(bot_id)
    await query.answer("تم إعادة تشغيل البوت 🔄", show_alert=True)
    await bot_info_cb(client, query)

@Client.on_callback_query(filters.regex(r"^botdelete_(\d+)$") & filters.user(factory_owners) & is_factory)
async def bot_delete_cb(client: Client, query: CallbackQuery):
    bot_id = query.data.split("_")[1]
    remove_bot(bot_id)
    await query.answer("تم حذف البوت وكل ملفاته 🗑", show_alert=True)
    await bots_list_cb(client, query)

@Client.on_callback_query(filters.regex(r"^bots_list$") & filters.user(factory_owners) & is_factory)
async def bots_list_cb(client: Client, query: CallbackQuery):
    bots = get_all_bots()
    if not bots:
        await query.message.edit_text("لا توجد بوتات مصنوعة حالياً.")
        return
        
    keyboard = []
    for b in bots:
        status_emoji = "🟢" if b['status'] == 'running' and is_process_running(b['pid']) else "🔴"
        keyboard.append([InlineKeyboardButton(f"{status_emoji} @{b['username']}", callback_data=f"botinfo_{b['id']}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await query.message.edit_text(f"📊 **البوتات المصنوعة:** {len(bots)}", reply_markup=reply_markup)
    except MessageNotModified:
        pass
