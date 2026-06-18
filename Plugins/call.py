import random, time, traceback, logging
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from config import r, Dev_Zaid
from helpers.Ranks import admin_pls, isLockCommand

logger = logging.getLogger("CALL")

call_phrases = [
    "اشتاقيت لعيونـڪ 🥺✨ : {mention}",
    "تعـا نورنـھَہّ يقمر 🌙 : {mention}",
    "تعـال شارڪ ويانھَہّ 🫶 : {mention}",
    "ويــن طامــس يحـلــو 🤔 : {mention}",
    "ممـڪن نتعــرف؟ 🫣 : {mention}",
    "مكانك خالي بالكروب 💔 : {mention}",
    "نورنا بوجودك يالزين 🌺 : {mention}",
    "وين الغيبة؟ ترا فاقدينك 🥺 : {mention}",
    "ياخي الكروب بدونك ظلام 🌑 : {mention}",
    "اطلع من الخاص وتعال اهنا 😂 : {mention}",
    "شدتسوي؟ تعال سولف ويانا 💬 : {mention}",
    "منورنا اليوم يا قمر 🌝 : {mention}",
    "اسمعني صوتك يا حلو 🎧 : {mention}",
    "شنو هالغيبة الطويلة؟ 😡 : {mention}",
    "فديت الطول والاسم الحلو 🌸 : {mention}",
    "وين رحت وعفتنا؟ ارجع بسرعة 🏃‍♂️ : {mention}",
    "تعال اشرب چاي ويانا ☕️ : {mention}",
    "لك وحشة والله، شخبارك؟ 🥰 : {mention}",
    "وينك يا اسطورة؟ الكروب نايم بدونك 😴 : {mention}",
    "يا هلا باللي طلته تسعد القلب ❤️ : {mention}"
]

def do_call(c, m, k):
    try:
        cid = m.chat.id
        fid = m.from_user.id
        
        logger.info(f"[CALL] بدء جلب الأعضاء للمجموعة {cid}")
        all_members = []
        
        # 1) البحث العشوائي
        search_chars = list("abcdefghijklmnopqrstuvwxyzابتثجحخدذرزسشصضطظعغفقكلمنهوي")
        random.shuffle(search_chars)
        
        for char in search_chars[:5]:
            try:
                # synchronous iteration because pyrogram is patched
                for member in c.get_chat_members(cid, query=char, limit=50):
                    user = member.user
                    if user.is_bot or user.is_deleted or user.id == fid or user.id == int(Dev_Zaid):
                        continue
                    all_members.append(user)
            except Exception as e:
                pass
                
        # 2) الجلب المباشر لو ما لقى شيء
        if not all_members:
            try:
                for member in c.get_chat_members(cid, limit=200):
                    user = member.user
                    if user.is_bot or user.is_deleted or user.id == fid or user.id == int(Dev_Zaid):
                        continue
                    all_members.append(user)
            except:
                pass
                
        if not all_members:
            return m.reply(f'{k} ما لكيت احد اناديه بالكروب 🥲')
        
        # إزالة التكرار
        seen = set()
        unique_members = []
        for u in all_members:
            if u.id not in seen:
                seen.add(u.id)
                unique_members.append(u)
        all_members = unique_members
        
        # اختيار عشوائي مع منع التكرار
        last_called = r.get(f'{cid}:last_call:{Dev_Zaid}')
        last_called = int(last_called) if last_called else 0
        
        random.shuffle(all_members)
        selected = all_members[0]
        if selected.id == last_called and len(all_members) > 1:
            selected = all_members[1]
            
        r.set(f'{cid}:last_call:{Dev_Zaid}', selected.id)
        
        mention = f"[{selected.first_name}](tg://user?id={selected.id})"
        phrase = random.choice(call_phrases)
        final_message = phrase.format(mention=mention)
        
        logger.info(f"[CALL] تم نداء {selected.first_name}")
        m.reply(final_message)
        
    except Exception as e:
        logger.error(f"[CALL] خطأ: {e}")
        logger.error(traceback.format_exc())
        try:
            m.reply(f'{k} حدث خطأ: `{str(e)}`')
        except:
            pass


@Client.on_message(filters.text & filters.group, group=8)
def call_member_handler(c, m):
    try:
        if not getattr(m, 'from_user', None): return
        
        text = m.text
        if not text: return
        
        name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
        if text.startswith(f'{name} '):
          text = text.replace(f'{name} ','')
          
        clean_text = text.strip()
        k = r.get(f'{Dev_Zaid}:botkey') or '⇜'
        
        if clean_text in ['تعطيل النداء', 'تعطيل نداء', 'قفل النداء']:
            if not admin_pls(m.from_user.id, m.chat.id):
                return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
            if r.get(f'{m.chat.id}:disableCall:{Dev_Zaid}'):
                return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} النداء معطل من قبل\n☆')
            else:
                r.set(f'{m.chat.id}:disableCall:{Dev_Zaid}', 1)
                return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت ميزة النداء\n☆')
                
        if clean_text in ['تفعيل النداء', 'تفعيل نداء', 'فتح النداء']:
            if not admin_pls(m.from_user.id, m.chat.id):
                return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
            if not r.get(f'{m.chat.id}:disableCall:{Dev_Zaid}'):
                return m.reply(f'「 {m.from_user.mention} 」\n{k} النداء مفعل من قبل\n☆')
            else:
                r.delete(f'{m.chat.id}:disableCall:{Dev_Zaid}')
                return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت ميزة النداء\n☆')

        if clean_text == 'نداء':
            if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
                return
            if r.get(f'{m.chat.id}:disableCall:{Dev_Zaid}'):
                return
                
            cid = m.chat.id
            fid = m.from_user.id
            if not admin_pls(fid, cid):
                return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
            
            Thread(target=do_call, args=(c, m, k)).start()
            
    except Exception as e:
        # Ignore StopPropagation
        if type(e).__name__ == 'StopPropagation':
            raise
        logger.error(f"[CALL] خطأ: {e}")
