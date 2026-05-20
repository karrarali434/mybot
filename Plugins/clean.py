import asyncio
import redis.asyncio as redis
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from config import token
import re

from helpers.Ranks import admin_pls
import config

chats_db = {}
db = redis.Redis(decode_responses=True)
ZAID = token.split(':')[0]

@Client.on_message(filters.regex(r"^مسح(\s+الميديا|\s+الكل)?(\s+\d+)?$") & filters.group, group=50)
async def manual_clean(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
        
    k = await db.get(f"{ZAID}:botkey") or "•"
    text = m.text.replace("مسح", "").strip()
    count = 100 # الافتراضي
    delete_type = "media" # الافتراضي
    
    if "الكل" in text:
        delete_type = "all"
        text = text.replace("الكل", "").strip()
    elif "الميديا" in text:
        delete_type = "media"
        text = text.replace("الميديا", "").strip()
        
    try:
        if text.isdigit():
            count = int(text)
            if count > 1000:
                count = 1000
    except:
        pass
        
    wait_msg = await m.reply(f"{k} جاري المسح...")
    deleted_count = 0
    msgs_to_delete = []
    
    try:
        message_ids = list(range(m.id - 1, m.id - count - 1, -1))
        for i in range(0, len(message_ids), 100):
            batch_ids = message_ids[i:i+100]
            try:
                msgs = await c.get_messages(m.chat.id, batch_ids)
                for msg in msgs:
                    if not msg or msg.empty:
                        continue
                        
                    if delete_type == "media":
                        if msg.media and not msg.audio and not msg.voice and not msg.game:
                            msgs_to_delete.append(msg.id)
                    else:
                        msgs_to_delete.append(msg.id)
                        
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass
                
            if len(msgs_to_delete) >= 100:
                try:
                    await c.delete_messages(m.chat.id, msgs_to_delete)
                    deleted_count += len(msgs_to_delete)
                    msgs_to_delete.clear()
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    pass
                    
        if msgs_to_delete:
            try:
                await c.delete_messages(m.chat.id, msgs_to_delete)
                deleted_count += len(msgs_to_delete)
            except Exception:
                pass
                
        await wait_msg.edit(f"{k} تم مسح {deleted_count} رسالة بنجاح.")
    except Exception as e:
        await wait_msg.edit(f"حدث خطأ أثناء المسح: {e}")

@Client.on_message(filters.regex(r"^(تفعيل|تعطيل) المسح$") & filters.group, group=51)
async def toggle_auto_clean(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
        
    k = await db.get(f"{ZAID}:botkey") or "•"
    if "تفعيل" in m.text:
        await db.hset(ZAID+str(m.chat.id), "ena-clean", "1")
        await m.reply(f"{k} تم تفعيل المسح التلقائي للرسائل بنجاح.\n\nلتغيير الوقت ارسل: وقت المسح [المدة]\nلتغيير النوع ارسل: نوع المسح [الكل/الميديا]")
    else:
        await db.hdel(ZAID+str(m.chat.id), "ena-clean")
        await m.reply(f"{k} تم تعطيل المسح التلقائي للرسائل بنجاح.")

@Client.on_message(filters.regex(r"^وقت المسح (\d+)(.*)$") & filters.group, group=52)
async def set_clean_time(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
        
    k = await db.get(f"{ZAID}:botkey") or "•"
    match = re.match(r"^وقت المسح (\d+)(.*)$", m.text.strip())
    if match:
        num = int(match.group(1))
        unit = match.group(2).strip()
        
        secs = num
        unit_name = "ثانية"
        if "دقيق" in unit or "دقائق" in unit:
            secs = num * 60
            unit_name = "دقيقة"
        elif "ساع" in unit:
            secs = num * 3600
            unit_name = "ساعة"
        elif "يوم" in unit or "ايام" in unit:
            secs = num * 86400
            unit_name = "يوم"
            
        await db.hset(ZAID+str(m.chat.id), "clean-secs", str(secs))
        await m.reply(f"{k} تم تعيين وقت المسح التلقائي إلى ( {num} {unit_name} ).")

@Client.on_message(filters.regex(r"^نوع المسح (الميديا|الكل)$") & filters.group, group=53)
async def set_clean_type(c: Client, m: Message):
    if not admin_pls(m.from_user.id, m.chat.id):
        return
        
    k = await db.get(f"{ZAID}:botkey") or "•"
    ctype = "media" if "الميديا" in m.text else "all"
    await db.hset(ZAID+str(m.chat.id), "clean-type", ctype)
    await m.reply(f"{k} تم تعيين نوع المسح التلقائي على: ( {'الميديا' if ctype == 'media' else 'الكل'} ).")

@Client.on_message(filters.group, group=54)
async def add_messages(c: Client, m: Message):
    if not getattr(m, 'from_user', None): return
    
    if await db.hget(ZAID+str(m.chat.id), "ena-clean"):
        ctype = await db.hget(ZAID+str(m.chat.id), "clean-type") or "media"
        
        is_target = False
        if ctype == "media":
            if m.media and not m.audio and not m.voice and not m.game:
                is_target = True
        else:
            is_target = True
            
        if is_target:
            if m.chat.id not in chats_db:
                chats_db[m.chat.id] = []
                
            secs = int(await db.hget(ZAID+str(m.chat.id), "clean-secs") or "60")
            time_now = datetime.now()
            
            if m.media_group_id:
                try:
                    msgs = await c.get_media_group(m.chat.id, m.id)
                    for msg in msgs:
                        data = {"id":msg.id, "time":time_now + timedelta(seconds=secs)}
                        # تجنب التكرار
                        if not any(d['id'] == msg.id for d in chats_db[m.chat.id]):
                            chats_db[m.chat.id].append(data)
                except:
                    data = {"id":m.id, "time":time_now + timedelta(seconds=secs)}
                    chats_db[m.chat.id].append(data)
            else:
                data = {"id":m.id, "time":time_now + timedelta(seconds=secs)}
                chats_db[m.chat.id].append(data)

async def auto_clean_function(c: Client):
    while True:
        await asyncio.sleep(2.0)
        try:
            time_now = datetime.now()
            for chat_id in list(chats_db.keys()):
                msgs_ids = []
                for msg in list(chats_db[chat_id]):
                    if time_now > msg["time"]:
                        msgs_ids.append(msg['id'])
                        try:
                            chats_db[chat_id].remove(msg)
                        except ValueError:
                            pass
                if msgs_ids:
                    # تقسيم الرسائل الى دفعات 100
                    for i in range(0, len(msgs_ids), 100):
                        batch = msgs_ids[i:i+100]
                        try:
                            await c.delete_messages(chat_id, batch)
                        except FloodWait as flood:
                            await asyncio.sleep(flood.value)
                        except Exception:
                            continue
        except Exception as e:
            print(f"Error in auto_clean_function: {e}")
