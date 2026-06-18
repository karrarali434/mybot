import re
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from config import r, Dev_Zaid
from helpers.Ranks import admin_pls, mod_pls, dev_pls, pre_pls

def Find(text):
    if not text:
        return []
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return [x[0] for x in url]

def has_link(m):
    entities = m.entities or m.caption_entities
    if entities:
        for ent in entities:
            if ent.type in [MessageEntityType.URL, MessageEntityType.TEXT_LINK, MessageEntityType.MENTION]:
                return True
    text = m.text or m.caption or ""
    if Find(text):
        return True
    return False

@Client.on_message(filters.text & filters.group, group=110)
def anti_manipulation_commands(c, m):
    if not getattr(m, 'from_user', None): return
    text = m.text
    name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    k = r.get(f'{Dev_Zaid}:botkey') or '⇜'

    if text == "تفعيل حماية التلاعب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if r.get(f"{m.chat.id}:anti_manipulation:{Dev_Zaid}"):
            return m.reply(f"{k} حماية التلاعب مفعله من قبل\n☆")
        r.set(f"{m.chat.id}:anti_manipulation:{Dev_Zaid}", 1)
        return m.reply(f"{k} ابشر فعلت حماية التلاعب\n☆")

    if text == "تعطيل حماية التلاعب":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if not r.get(f"{m.chat.id}:anti_manipulation:{Dev_Zaid}"):
            return m.reply(f"{k} حماية التلاعب معطله من قبل\n☆")
        r.delete(f"{m.chat.id}:anti_manipulation:{Dev_Zaid}")
        return m.reply(f"{k} ابشر عطلت حماية التلاعب\n☆")

@Client.on_edited_message(filters.group, group=111)
def anti_manipulation_edited(c, m):
    if not getattr(m, 'from_user', None): return
    if not r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if not r.get(f"{m.chat.id}:anti_manipulation:{Dev_Zaid}"): return
    
    if admin_pls(m.from_user.id, m.chat.id): return
    
    contains_link = has_link(m)
    
    if contains_link:
        k = r.get(f'{Dev_Zaid}:botkey') or '⇜'
        mention = m.from_user.mention
        try:
            m.delete()
        except:
            pass
        return m.reply(f"「 {mention} 」\n{k} تنبيه: هذا العضو يتلاعب بالرسائل وقام بتعديلها وإضافة رابط أو صورة!\nتم حذف الرسالة لحماية القروب.\n☆", disable_web_page_preview=True)
