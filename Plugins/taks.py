from pyrogram import Client, filters
from pyrogram.types import Message
from config import r, Dev_Zaid
from helpers.Ranks import admin_pls
import re

@Client.on_message(filters.regex(r"^اضف تاك$") & filters.group, group=70)
def start_add_tak(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
    k = r.get(f"{Dev_Zaid}:botkey") or "•"
    r.set(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}", "wait_name")
    m.reply(f"{k} أرسل الآن الكلمة (الاسم) الذي تريده للتاك.\n- أرسل `الغاء` لإلغاء العملية.")

@Client.on_message(filters.group & ~filters.bot, group=71)
def process_tak_state(c: Client, m: Message):
    if not m.text: return
    if m.text == "اضف تاك": return # تجاهل نفس الرسالة التي بدأت الأمر
    
    state = r.get(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}")
    k = r.get(f"{Dev_Zaid}:botkey") or "•"
    
    if state == "wait_name":
        if m.text == "الغاء":
            r.delete(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}")
            return m.reply(f"{k} تم الإلغاء.")
            
        keyword = m.text.strip()
        r.set(f"{m.chat.id}:TakKeyword:{m.from_user.id}{Dev_Zaid}", keyword)
        r.set(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}", "wait_user")
        return m.reply(f"{k} حسناً، أرسل الآن يوزر الشخص (مثال: @username).\n- أرسل `الغاء` لإلغاء العملية.")
        
    elif state == "wait_user":
        if m.text == "الغاء":
            r.delete(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}")
            r.delete(f"{m.chat.id}:TakKeyword:{m.from_user.id}{Dev_Zaid}")
            return m.reply(f"{k} تم الإلغاء.")
            
        username = m.text.strip()
        if not username.startswith("@"):
            return m.reply(f"{k} عذراً، الرجاء إرسال اليوزر بشكل صحيح مبدوءاً بـ @")
            
        keyword = r.get(f"{m.chat.id}:TakKeyword:{m.from_user.id}{Dev_Zaid}")
        # Save to hash
        r.hset(f"{Dev_Zaid}taks:{m.chat.id}", keyword, username)
        
        r.delete(f"{m.chat.id}:TakState:{m.from_user.id}{Dev_Zaid}")
        r.delete(f"{m.chat.id}:TakKeyword:{m.from_user.id}{Dev_Zaid}")
        
        return m.reply(f"{k} تم حفظ التاك بنجاح!\nالكلمة: {keyword}\nاليوزر: {username}")

@Client.on_message(filters.text & filters.group & ~filters.bot, group=72)
def watch_taks(c: Client, m: Message):
    # Only check if it's not a command
    if m.text.startswith("/") or m.text.startswith("اضف") or m.text.startswith("حذف"):
        pass # Allow them to trigger if they have tags containing these words, but usually ignored
        
    taks = r.hgetall(f"{Dev_Zaid}taks:{m.chat.id}")
    if not taks:
        return
        
    text_lower = m.text.lower()
    for keyword, username in taks.items():
        if keyword.lower() in text_lower:
            try:
                m.reply(f"جابوك بالطاري {username}")
                break # Avoid multiple mentions for the same message
            except:
                pass

@Client.on_message(filters.regex(r"^(حذف|مسح) تاك (.*)$") & filters.group, group=73)
def delete_tak(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
    k = r.get(f"{Dev_Zaid}:botkey") or "•"
    keyword = m.matches[0].group(2).strip()
    res = r.hdel(f"{Dev_Zaid}taks:{m.chat.id}", keyword)
    if res:
        m.reply(f"{k} تم حذف التاك ( {keyword} ) بنجاح.")
    else:
        m.reply(f"{k} التاك غير موجود في القائمة.")
        
@Client.on_message(filters.regex(r"^مسح التاكات$") & filters.group, group=75)
def clear_all_taks(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
    k = r.get(f"{Dev_Zaid}:botkey") or "•"
    res = r.delete(f"{Dev_Zaid}taks:{m.chat.id}")
    if res:
        m.reply(f"{k} تم مسح جميع التاكات في هذه المجموعة بنجاح.")
    else:
        m.reply(f"{k} لا توجد تاكات محفوظة لمسحها.")
        
@Client.on_message(filters.regex(r"^التاكات$") & filters.group, group=74)
def list_taks(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
    k = r.get(f"{Dev_Zaid}:botkey") or "•"
    taks = r.hgetall(f"{Dev_Zaid}taks:{m.chat.id}")
    if not taks:
        return m.reply(f"{k} لا توجد تاكات محفوظة في هذه المجموعة.")
        
    msg = f"{k} قائمة التاكات:\n\n"
    for idx, (kw, user) in enumerate(taks.items(), 1):
        msg += f"{idx} - {kw} ↢ {user}\n"
    m.reply(msg)
