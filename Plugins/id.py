import random, re, time, os
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.get_create import get_creation_date
from pyrogram.raw.functions.users import GetFullUser
from io import BytesIO
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.raw.functions.channels import GetFullChannel
from .games import get_emoji_bank
from helpers.Ranks import isLockCommand
def get_top(users):
   users = [tuple(i.items()) for i in users]
   top = sorted(users, key=lambda i: i[-1][-1], reverse=True)
   top = [dict(i) for i in top]
   return top
custom_ids = ['''
- ᴜѕᴇʀɴᴀᴍᴇ ➣ {اليوزر} .
- ᴍѕɢѕ ➣ {الرسائل} .
- ѕᴛᴀᴛѕ ➣ {الرتبه} .
- ʏᴏᴜʀ ɪᴅ ➣ {الايدي} .
- ᴇᴅɪᴛ ᴍsɢ ➣ {التعديل} .
- ᴅᴇᴛᴀɪʟs ➣ {التفاعل} .
-  ɢᴀᴍᴇ ➣ {المجوهرات} .
{البايو}
''','''
• USE 𖦹 {اليوزر}
• MSG 𖥳 {الرسائل}
• STA 𖦹 {الرتبه}
• iD 𖥳 {الايدي}
{البايو}
''','''
➞: 𝒔𝒕𝒂𓂅 {اليوزر} 𓍯
➞: 𝒖𝒔𝒆𝒓𓂅 {المعرف} 𓍯
➞: 𝒎𝒔𝒈𝒆𓂅 {الرسائل} 𓍯
➞: 𝒊𝒅 𓂅 {الايدي} 𓍯
{البايو}
''','''
♡ : 𝐼𝐷 𖠀 {الايدي} .
♡ : 𝑈𝑆𝐸𝑅 𖠀 {اليوزر} .
♡ : 𝑀𝑆𝐺𝑆 𖠀 {الرسائل} .
♡ : 𝑆𝑇𝐴𝑇𝑆 𖠀 {الرتبه} .
♡ : 𝐸𝐷𝐼𝑇  𖠀 {التعديل} .
{البايو}
''', '''
- الايـدي || {الايدي}.
• الاسـم  || {الاسم}.
• المُعرف || {اليوزر}.
• الرُتبـه || {الرتبه}.
• الرسائل || {الرسائل}.
{البايو}
''', '''
⌁ NaMe ⇨ {الاسم}
⌁ Use ⇨ {اليوزر}
⌁ Msg ⇨ {الرسائل}
⌁ Sta ⇨ {الرتبه}
⌁ iD ⇨ {الايدي}
{البايو}
''', '''
📋¦ ɴᴀᴍᴇ ➺ {الاسم}
🗞¦ ʏᴏᴜʀ ɪᴅ ➺ {الايدي}
🔦¦ ᴜѕᴇʀɴᴀᴍᴇ ➺ {اليوزر}
🕹¦ ѕᴛᴀᴛѕ ➺ {الرتبه}
🔭¦ ᴅᴇᴛᴀɪʟs ➺ {التفاعل}
📨¦  ᴍѕɢѕ ➺ {الرسائل}
🎰¦ ɢᴀᴍᴇ ➺ {المجوهرات}
{البايو}
''', '''
✾ 𝐔𝐒𝐄 ⤷ {اليوزر}
✾ 𝐌𝐒𝐆 ⤷ {الرسائل}
✾ 𝐒𝐓𝐀 ⤷ {الرتبه}
✾ 𝐈𝐃 ⤷ {الايدي}
✾ 𝐁𝐈𝐎 ⤷ {البايو}
''', '''
𓆰 𝑼𝑬𝑺 : {اليوزر}
𓆰 𝑺𝑻𝑨 : {الرتبه}
𓆰 𝑰𝑫 : {الايدي}
𓆰 𝑴𝑺𝑮 : {الرسائل}
{البايو}'''
]


comments = [
  'تيكفه لاتكتب ايدي',
  'يع',
  'جبر',
  'احلى من يكتب ايدي',
  'افخم ايدي',
  'لحد يرسل ايدي من بعده',
  'يلبييه اطلق ايدي',
  'ازق ايدي',
  'لعد تكتب ايدي',
  'للاسف ايديك تلوث بصري ):',
  'جابك الله انت وأيديك على شكل جبر خاطر لقلبّي'
]

@Client.on_message(filters.group, group=9)
def addmsgCount(c,m):
   if not getattr(m, 'from_user', None): return
   if not getattr(m, "from_user", None): return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
   if not r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}'):
      r.set(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}', 1)
   else:
      get = int(r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}'))
      r.set(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}', get+1)
   r.set(f"{m.from_user.id}:bankName", m.from_user.first_name[:25])

@Client.on_edited_message(filters.group, group=10)
def addeditedmsgCount(c,m):
   if not getattr(m, 'from_user', None): return

   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
   if not r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'):
      r.set(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}', 1)
   else:
      get = int(r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'))
      r.set(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}', get+1)

@Client.on_message(filters.text & filters.group, group=11)
def rankGetHandler(c,m):
   if not getattr(m, 'from_user', None): return
   k = r.get(f'{Dev_Zaid}:botkey')
   Thread(target=get_my_rank,args=(c,m,k)).start()



def get_my_rank(c,m,k):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_Zaid}'):  return
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   if isLockCommand(m.from_user.id, m.chat.id, text): return
   if text == 'مجموعاتي':
     if not r.smembers(f'{m.from_user.id}:groups'):
       return m.reply(f'{k} ماعندك مجموعات')
     else:
       groups = len(r.smembers(f'{m.from_user.id}:groups'))
       return m.reply(f'{k} عدد مجموعاتك ↼ ( {groups} )')

   if text == 'انشائي':
      create_date = get_creation_date(m.from_user.id)
      return m.reply(f'{k} الانشاء ( {create_date} )')

   if text == 'الانشاء' and not m.reply_to_message:
      create_date = get_creation_date(m.from_user.id)
      return m.reply(f'{k} الانشاء ( {create_date} )')

   if (text == 'الانشاء' or text == 'انشائه') and m.reply_to_message:
      create_date = get_creation_date(m.reply_to_message.from_user.id)
      return m.reply(f'{k} الانشاء ( {create_date} )')

   if text.startswith('انشاء ') and len(text.split()) == 2:
      try:
        user_input = text.split()[1]
        try:
          user_id = int(user_input)
        except:
          user_id = user_input.replace('@', '')
        get_user = c.get_chat(user_id)
        create_date = get_creation_date(get_user.id)
        return m.reply(f'{k} انشاء [{get_user.first_name}](tg://user?id={get_user.id}) ↢ ( {create_date} )', disable_web_page_preview=True)
      except Exception:
        return m.reply(f'{k} ماقدرت اجيب معلومات هالشخص')

   if text == 'اسمي':
     return m.reply(m.from_user.first_name, disable_web_page_preview=True)

   if text == 'معلوماتي':
      try:
         msgs_raw = r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}')
         msgs = int(msgs_raw) if msgs_raw else 0
         if msgs > 10000:
            tfa3l = 'كنق التلي'
         elif msgs > 5000:
            tfa3l = 'اسطورة التفاعل'
         elif msgs > 2500:
            tfa3l = 'متفاعل'
         elif msgs > 750:
            tfa3l = 'تفاعل متوسط'
         elif msgs > 500:
            tfa3l = 'يجي منك'
         elif msgs > 50:
            tfa3l = 'شد حيلك'
         else:
            tfa3l = 'تفاعل صفر'
         if not r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'):
            edits = 0
         else:
            edits= int(r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'))
         if not r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'):
            contacts = 0
         else:
            contacts = int(r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'))
         if m.from_user.username:
            username = f'@{m.from_user.username}'
         elif getattr(m.from_user, 'usernames', None):
            username = ''
            for i in m.from_user.usernames: username += f"@{i.username} "
         else:
            username = 'مافي يوزر'
         rank = get_rank(m.from_user.id,m.chat.id)
         try:
            get_bio = c.get_chat(m.from_user.id)
            bio = get_bio.bio if get_bio.bio else 'مافي بايو'
         except:
            bio = 'مافي بايو'
         text = f'''
⚘ المعلومات
❁ الاسم ↼ {m.from_user.mention}
❁ اليوزر ↼ {username}
❁ الايدي  ↼ {m.from_user.id}
❁ الرتبه ↼ {rank}
❁ البايو ↼ {bio}
┄─┅═ـ═┅─┄
⚘ احصائيات الرسايل
❁ الرسايل ↼ {msgs}
❁ التعديل ↼ {edits}
❁ التفاعل ↼ {tfa3l}
'''
         return m.reply(text)
      except Exception as e:
         print(f"[معلوماتي ERROR] {e}")
         return m.reply(f'{k} حدث خطأ أثناء جلب معلوماتك')

   if text == 'بايو' and m.reply_to_message and m.reply_to_message.from_user:
      if r.get(f'{m.chat.id}:disableBio:{Dev_Zaid}'): return m.reply(f'{k} عذراً البايو مغلق')
      get = c.get_chat(m.reply_to_message.from_user.id)
      if not get.bio:
        return m.reply(f'{k} ماعنده بايو')
      else:
        return m.reply(f'`{get.bio}`')

   if text == 'بايو' and not m.reply_to_message:
      if r.get(f'{m.chat.id}:disableBio:{Dev_Zaid}'): return m.reply(f'{k} عذراً البايو مغلق')
      get = c.get_chat(m.from_user.id)
      if not get.bio:
        return m.reply(f'{k} ماعندك بايو')
      else:
        return m.reply(f'`{get.bio}`')


   if text == 'المجموعه' or text == 'المجموعة':
      if not owner_pls(m.from_user.id, m.chat.id):
         return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      get = c.invoke(GetFullChannel(channel=c.resolve_peer(m.chat.id)))
      if get.full_chat.exported_invite:
        link = get.full_chat.exported_invite.link
      else:
        link = 'مافي رابط'
      admins = get.full_chat.admins_count
      kicked = get.full_chat.kicked_count
      count = get.full_chat.participants_count
      if m.chat.photo:
        type = 'photo'
        if m.chat.username:
          photo = f'https://t.me/{m.chat.username}'
        else:
          photo = c.download_media(m.chat.photo.big_file_id)
      else:
        type = 'text'
      text = f'معلومات المجموعة:\n\n{k} الاسم ↢ {m.chat.title}\n{k} الايدي ↢ {m.chat.id}\n{k} عدد الاعضاء ↢ ( {count} )\n{k} عدد المشرفين ↢ ( {admins} )\n{k} عدد المحظورين ↢ ( {kicked} )\n{k} الرابط ↢ {link} '
      if type == 'photo':
         m.reply_photo(photo, caption=text)
         try:
           os.remove(photo)
         except:
           pass
         return
      else:
         return m.reply(text, disable_web_page_preview=True)

   if text == 'جهاتي':
     if not r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'):
       contacts = 0
     else:
       contacts = int(r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'))
     return m.reply(f'{k} عدد جهاتك ↢ {contacts}')

   if text in ['افتاري', 'صورتي']:
     if not pre_pls(m.from_user.id, m.chat.id):
       return m.reply(f'{k} هذا الامر يخص ( المميز وفوق ) بس')
     if r.get(f'{m.chat.id}:disableAV:{Dev_Zaid}'): return m.reply(f'{k} عذراً الافتار مغلق')
     if not m.from_user.photo:
       return m.reply(f'{k} ماقدر اجيب افتارك ارسل نقطه خاص وارجع جرب')
     else:
       if m.from_user.username:
         photo = f'http://t.me/{m.from_user.username}'
       else:
         for p in c.get_chat_photos(m.from_user.id,limit=1):
           photo = p.file_id
       get_bio = c.get_chat(m.from_user.id).bio
       if not get_bio:
         caption=None
       else:
         caption = f'`{get_bio}`'
       return m.reply_photo(photo,caption=caption)

   if text in ['افتار', 'صورته'] and m.reply_to_message and m.reply_to_message.from_user:
     if not pre_pls(m.from_user.id, m.chat.id):
       return m.reply(f'{k} هذا الامر يخص ( المميز وفوق ) بس')
     if r.get(f'{m.chat.id}:disableAV:{Dev_Zaid}'): return m.reply(f'{k} عذراً الافتار مغلق')
     if not m.reply_to_message.from_user.photo:
       return m.reply(f'{k} مقدر اجيب افتاره يمكن حاظرني')
     else:
       if m.reply_to_message.from_user.username:
         photo = f'http://t.me/{m.reply_to_message.from_user.username}'
       else:
         for p in c.get_chat_photos(m.reply_to_message.from_user.id,limit=1):
           photo = p.file_id
       get_bio = c.get_chat(m.reply_to_message.from_user.id).bio
       if not get_bio:
         caption=None
       else:
         caption = f'`{get_bio}`'
       return m.reply_photo(photo,caption=caption)

   if text == 'ايديي':
     return m.reply(f'( `{m.from_user.id}` )')

   if text.startswith('افتار') and len(text.split()) == 2:
     if r.get(f'{m.chat.id}:disableAV:{Dev_Zaid}'): return m.reply(f'{k} عذراً الافتار مغلق')
     try:
       user = int(text.split()[1])
     except:
       user = text.split()[1]
     try:
       get = c.get_users(user.lstrip('@'))
       if get.photo:
         for p in c.get_chat_photos(get.id,limit=1):
           photo = p.file_id
         if get.bio:
           caption = f'`{get.bio}`'
         else:
           caption = None
         return m.reply_photo(photo,caption=caption)
     except Exception as e:
       print (e)
       return


   if text == 'رتبتي':
      rank = get_rank(m.from_user.id, m.chat.id)
      m.reply(f'{k} رتبتك ↢ {rank}')

   if text == 'مسح رسائلي' or text == 'مسح رسايلي':
      msgs = int(r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}'))
      r.delete(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}')
      return m.reply(f'{k} ابشر مسحت ( {msgs} ) من رسائلك')

   if text == 'مسح تكليجاتي':
      if not r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'):
        return m.reply(f'{k} عدد تكليجاتك ↢ 0')
      msgs = int(r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'))
      r.delete(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}')
      return m.reply(f'{k} ابشر مسحت ( {msgs} ) من تكليجاتك')

   if text == 'تكليجاتي' or text == 'تعديلاتي':
      if not r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'):
        return m.reply(f'{k} عدد تكليجاتك ↢ 0')
      msgs = int(r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'))
      return m.reply(f'{k} عدد تكليجاتك ↢ {msgs}')

   if text == 'رسايلي' or text == 'رسائلي':
      msgs = int(r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}'))
      return m.reply(f'{k} عدد رسايلك ↢ {msgs}')
      
   if (text == 'رسايله' or text == 'رسائلة') and m.reply_to_message and m.reply_to_message.from_user:
      msgs = int(r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.reply_to_message.from_user.id}'))
      return m.reply(f'{k} عدد رسايله ↢ {msgs}')




   if text in ['رتبته', 'لقبه'] and m.reply_to_message and m.reply_to_message.from_user:
      rank = get_rank(m.reply_to_message.from_user.id, m.chat.id)
      member = m.chat.get_member(m.reply_to_message.from_user.id)
      status = member.status
      if status == ChatMemberStatus.OWNER:
        rank2 = 'المالك'
      if status == ChatMemberStatus.ADMINISTRATOR:
        rank2 = 'مشرف'
      if status == ChatMemberStatus.RESTRICTED:
        rank2 = 'مقيد'
      if status == ChatMemberStatus.LEFT:
        rank2 = 'طالع'
      if status == ChatMemberStatus.MEMBER:
        rank2 = 'عضو'
      if status == ChatMemberStatus.BANNED:
        rank2 = 'لاقم حظر'
      if text == 'لقبه':
          title = getattr(member, 'custom_title', None) or rank2
          m.reply(f'{k} لقبه ↢ ( {title} )')
      else:
          m.reply(f'رتبته:\n{k} في البوت ( {rank} )\n{k} في المجموعة ( {rank2} )\n-')

   if text == 'نقل ملكية' or text == 'نقل ملكيه':
     if r.get(f'{m.chat.id}:rankGOWNER:{m.from_user.id}{Dev_Zaid}'):
       status = m.chat.get_member(m.from_user.id).status
       if status == ChatMemberStatus.OWNER:
          return m.reply(f'{k} انت مالك القروب')
       else:
          for member in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
              if member.user.is_deleted:
                return m.reply(f'{k} حساب المالك محذوف')
              else:
                r.delete(f'{m.chat.id}:rankGOWNER:{m.from_user.id}{Dev_Zaid}')
                r.srem(f'{m.chat.id}:listGOWNER:{Dev_Zaid}', m.from_user.id)
                r.set(f'{m.chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}')
                r.sadd(f'{m.chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
                return m.reply(f'「 {member.user.mention} 」\n{k} نقلت له ملكية المجموعة')

   if text == "مسح المتفاعلين" or text == "تصفير المتفاعلين":
     if not owner_pls(m.from_user.id, m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 المالك 〗فقط .')
     else:
       keys = r.keys(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:*")
       for _ in keys: r.delete(_)
       return m.reply(f"{k} ابشر مسحت كل المتفاعلين")

   if text == "مسح القروبات" or text == "تصفير القروبات":
     if not devp_pls(m.from_user.id, m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 Dev🎖️ 〗فقط .')
     else:
       keys = r.keys(f"{Dev_Zaid}:TotalGroupMsgs:*")
       for _ in keys: r.delete(_)
       return m.reply(f"{k} ابشر مسحت توب القروبات")

   if text == "ترتيبي" or text == "تفاعلي":
     users = r.keys(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:*")
     jj = []
     for user in users:
          try:
            id = int(user.split("TotalMsgs:")[1])
            msgs = r.get(user)
            jj.append({"id": id, "msgs": int(msgs)})
          except:
            pass
     top = get_top(jj)
     ids = [i["id"] for i in top]
     rank = ids.index(m.from_user.id) + 1
     msgs = int(r.get(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}"))
     return m.reply(f"{k} ترتيبك بالمتفاعلين ↢ {rank}\n{k} رسائلك بالتفاعل ↢ {msgs:,}\n-")

   if text == "المتفاعلين" or text == "توب المتفاعلين":
        if not admin_pls(m.from_user.id, m.chat.id):
            return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فما فوق .')
        users = r.keys(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:*")
        jj = []
        for user in users:
                  try:
                    id = int(user.split("TotalMsgs:")[1])
                    msgs = r.get(user)
                    name = r.get(f"{id}:bankName") or str(id)
                    jj.append({"name": name, "id": id, "msgs": int(msgs)})
                  except:
                    pass
        top = get_top(jj)
        if not top:
            return m.reply(f'{k} لا يوجد متفاعلين حالياً.')
        total_msgs = sum(i['msgs'] for i in top)
        text = f"📊 | إحصائيات تفاعل المجموعة\n"
        text += f"━━━━━━━━━━━━━━━━\n"
        text += f"👥 | عدد المتفاعلين ↢ {len(top)}\n"
        text += f"💬 | إجمالي الرسائل ↢ {total_msgs:,}\n"
        text += f"━━━━━━━━━━━━━━━━\n\n"
        count = 1
        for i in top:
            if count == 31: break
            emoji = get_emoji_bank(count)
            msgs_count = i['msgs']
            if msgs_count > 10000:
                tfa3l = 'طاك، مسيطر عالساحة 👑'
            elif msgs_count > 5000:
                tfa3l = '24 ساعة بالكروب، ما تنام؟ 🔥'
            elif msgs_count > 2500:
                tfa3l = 'عاش، مبدع وربي ⭐'
            elif msgs_count > 750:
                tfa3l = 'خوش تفاعل، استمر يابطل 📈'
            elif msgs_count > 50:
                tfa3l = 'يرادلك شده، نايم ورجليك بالشمس 📉'
            else:
                tfa3l = 'هذا بس يباوع، مزهرية 💤'
            
            text += f"{emoji}[{i['name']}](tg://user?id={i['id']}) ↢ {msgs_count:,} رسالة\n"
            text += f"  └ {tfa3l}\n\n"
            count +=1
        return c.send_message(m.chat.id, text, disable_web_page_preview=True, reply_to_message_id=m.id)

   if text == "تفاعل المشرفين" or text == "المشرفين المتفاعلين":
        if not admin_pls(m.from_user.id, m.chat.id):
            return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فما فوق .')
        try:
           admins_ids = []
           for mm in c.get_chat_members(m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
               if not mm.user.is_deleted and not mm.user.is_bot:
                   admins_ids.append(mm.user.id)
        except:
           admins_ids = []
           
        users = r.keys(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:*")
        jj = []
        for user in users:
                  try:
                    id = int(user.split("TotalMsgs:")[1])
                    if id in admins_ids or admin_pls(id, m.chat.id):
                        msgs = r.get(user)
                        name = r.get(f"{id}:bankName") or str(id)
                        jj.append({"name": name, "id": id, "msgs": int(msgs)})
                  except:
                    pass
        top = get_top(jj)
        if not top:
            return m.reply(f'{k} لا يوجد مشرفين متفاعلين حالياً.')
        total_msgs = sum(i['msgs'] for i in top)
        text = f"🛡 | إحصائيات تفاعل المشرفين\n"
        text += f"━━━━━━━━━━━━━━━━\n"
        text += f"👥 | عدد المشرفين ↢ {len(top)}\n"
        text += f"💬 | إجمالي الرسائل ↢ {total_msgs:,}\n"
        text += f"━━━━━━━━━━━━━━━━\n\n"
        count = 1
        for i in top:
            if count == 31: break
            emoji = get_emoji_bank(count)
            msgs_count = i['msgs']
            if msgs_count > 10000:
                tfa3l = 'طاك، مسيطر عالساحة 👑'
            elif msgs_count > 5000:
                tfa3l = '24 ساعة بالكروب، ما تنام؟ 🔥'
            elif msgs_count > 2500:
                tfa3l = 'عاش، مبدع وربي ⭐'
            elif msgs_count > 750:
                tfa3l = 'خوش تفاعل، استمر يابطل 📈'
            elif msgs_count > 50:
                tfa3l = 'يرادلك شده، نايم ورجليك بالشمس 📉'
            else:
                tfa3l = 'هذا بس يباوع، مزهرية 💤'
            
            text += f"{emoji}[{i['name']}](tg://user?id={i['id']}) ↢ {msgs_count:,} رسالة\n"
            text += f"  └ {tfa3l}\n\n"
            count +=1
        return c.send_message(m.chat.id, text, disable_web_page_preview=True, reply_to_message_id=m.id)

   if text == "القروبات" or text == "توب القروبات":
        groups = r.keys(f"{Dev_Zaid}:TotalGroupMsgs:*")
        result = []

        for group in groups:
            try:
                chat_id = int(group.split("TotalGroupMsgs:")[1])
                msgs = r.get(group)
                group_title = c.get_chat(chat_id).title
                result.append({"group_title": group_title, "chat_id": chat_id, "msgs": int(msgs)})
            except:
                pass

        top_groups = get_top(result)
        response_text = "- توب اكثر 20 قروب متفاعل:\n━━━━━━━━━\n"
        count = 1

        for group in top_groups:
            if count == 21:
                break
            emoji = get_emoji_bank(count)
            response_text += f"{emoji}{group['msgs']:,} l {group['group_title']}\n"
            count += 1

        return c.send_message(m.chat.id, response_text, disable_web_page_preview=True, reply_to_message_id=m.id)


   if text.startswith('كشف'):
       target_user = None
       ks = None
       if text == 'كشف' and m.reply_to_message and getattr(m.reply_to_message, 'from_user', None):
           target_user = m.reply_to_message.from_user.id
           ks = 'بالرد'
       elif len(text.split()) > 1 and m.text and m.text.html and 'tg://user?id=' in m.text.html:
           try:
               target_user = int(re.search(r'href="([^"]+)', m.text.html).group(1).split('=')[1])
               ks = 'بالمنشن'
           except: pass
       elif len(text.split()) == 2:
           try:
               target_user = int(text.split()[1])
               ks = 'بالايدي'
           except:
               target_user = text.split()[1].replace('@', '')
               ks = 'باليوزر'

       if target_user:
           try:
               try:
                   get = m.chat.get_member(target_user)
                   user_obj = get.user
                   status = get.status
               except:
                   user_obj = c.get_users(target_user)
                   status = ChatMemberStatus.LEFT
               
               name = user_obj.first_name
               id = user_obj.id
               
               msgs_str = r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{id}')
               msgs = int(msgs_str) if msgs_str else 0

               if user_obj.username:
                   username = f'@{user_obj.username}'
               elif getattr(user_obj, "usernames", None):
                   username = ""
                   for i in user_obj.usernames: username += f"@{i.username} "
               else:
                   username = 'مافي يوزر'
               
               if status == ChatMemberStatus.OWNER:
                   rank2 = 'المالك'
               elif status == ChatMemberStatus.ADMINISTRATOR:
                   rank2 = 'مشرف'
               elif status == ChatMemberStatus.RESTRICTED:
                   rank2 = 'مقيد'
               elif status == ChatMemberStatus.LEFT:
                   rank2 = 'طالع'
               elif status == ChatMemberStatus.MEMBER:
                   rank2 = 'عضو'
               elif status == ChatMemberStatus.BANNED:
                   rank2 = 'لاقم حظر'
               else:
                   rank2 = 'غير معروف'
               
               rank = get_rank(id, m.chat.id)
               create_date = get_creation_date(id)
               
               text_reply = f'''
{k} الاسم ↢ {name}
{k} الايدي ↢ {id}
{k} اليوزر : ↢ ( {username} ) 
{k} الرتبه ↢ ( {rank} )
{k} الرسائل ↢ ( {msgs} )
{k} تاريخ الانضمام ↢ ( {create_date} )
{k} بالمجموعة ↢ ( {rank2} )
{k} نوع الكشف ↢ {ks}
-
'''
               if not r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}') and user_obj.photo:
                   try:
                       for p in c.get_chat_photos(id, limit=1):
                           photo = p.file_id
                       return m.reply_photo(photo, caption=text_reply)
                   except:
                       return m.reply(text_reply, disable_web_page_preview=True)
               else:
                   return m.reply(text_reply, disable_web_page_preview=True)
           except Exception as e:
               print(e)
               return m.reply(f'{k} العضو مو بالمجموعة او معلوماته غير متاحة')
       elif text == 'كشف':
           # Tell the user how to use it correctly
           m.reply(f'{k} يرجى الرد على رسالة الشخص أو كتابة: كشف + الايدي/اليوزر')
           m.stop_propagation()
           return


   if text == 'صلاحياته' and m.reply_to_message and m.reply_to_message.from_user:
      get = m.chat.get_member(m.reply_to_message.from_user.id)
      if not get.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]:
         return m.reply(f'{k} هو العضو وما عنده صلاحيات')
      if get.status == ChatMemberStatus.OWNER:
         return m.reply(f'{k} هو المالك وعنده كل الصلاحيات')
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p = get.privileges
         p1 = "✔️" if p.can_manage_chat else "✖️"
         p2 = "✔️" if p.can_delete_messages else "✖️"
         p3 = "✔️" if p.can_manage_video_chats else "✖️"
         p4 = "✔️" if p.can_restrict_members else "✖️"
         p5 = "✔️" if p.can_promote_members else "✖️"
         p6 = "✔️" if p.can_change_info else "✖️"
         p7 = "✔️" if p.can_pin_messages else "✖️"
         text = f'''
{k} هو مشرف وهذي صلاحياته :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return m.reply(text)

   if text == 'صلاحياتي':
      get = m.chat.get_member(m.from_user.id)
      if not get.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]:
         return m.reply(f'{k} انت العضو وماعندك صلاحيات')
      if get.status == ChatMemberStatus.OWNER:
         return m.reply(f'{k} انت المالك وعندك كل الصلاحيات')
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p = get.privileges
         p1 = "✔️" if p.can_manage_chat else "✖️"
         p2 = "✔️" if p.can_delete_messages else "✖️"
         p3 = "✔️" if p.can_manage_video_chats else "✖️"
         p4 = "✔️" if p.can_restrict_members else "✖️"
         p5 = "✔️" if p.can_promote_members else "✖️"
         p6 = "✔️" if p.can_change_info else "✖️"
         p7 = "✔️" if p.can_pin_messages else "✖️"
         text = f'''
{k} انت مشرف وهذي صلاحياتك :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return m.reply(text)


   if r.get(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_Zaid}')
     m.reply(f'{k} ابشر تم الغاء تعيين الايدي ')
     return

   if r.get(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_Zaid}')
     m.reply(f'{k} ابشر تم الغاء تعيين الايدي عام')
     return

   if r.get(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_Zaid}') and dev_pls(m.from_user.id, m.chat.id):
      r.set(f'customID:{Dev_Zaid}', m.text)
      m.reply(f'{k} وسوينا الايدي العام\n{k} يمديك تجرب شكل الايدي الجديد الحين')
      r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_Zaid}')
      return

   if r.get(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_Zaid}') and mod_pls(m.from_user.id, m.chat.id):
      r.set(f'{m.chat.id}:customID:{Dev_Zaid}', m.text)
      m.reply(f'{k} وسوينا الايدي\n{k} يمديك تجرب شكل الايدي الجديد الحين')
      r.delete(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_Zaid}')
      return

   if text == 'مسح الايدي':
      if not mod_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      if not r.get(f'{m.chat.id}:customID:{Dev_Zaid}'):
        return m.reply(f'{k} الايدي مو معدل')
      else:
        m.reply(f'{k} ابشر مسحت الايدي')
        r.delete(f'{m.chat.id}:customID:{Dev_Zaid}')
        return

   if text == 'مسح الايدي العام' or text == 'مسح الايدي عام':
      if not dev2_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} عذراً الامر يخص ↤〖 Dev²🎖 〗فقط .')
      if not r.get(f'customID:{Dev_Zaid}'):
        return m.reply(f'{k} الايدي العام مو معدل')
      else:
        m.reply(f'{k} ابشر مسحت الايدي العام')
        r.delete(f'customID:{Dev_Zaid}')

   if text == 'الايدي':
      if not mod_pls(m.from_user.id, m.chat.id):
        return
      if not r.get(f'{m.chat.id}:customID:{Dev_Zaid}'):
        return m.reply(f'{k} الايدي مو معدل')
      else:
        id = r.get(f'{m.chat.id}:customID:{Dev_Zaid}')
        return m.reply(f'`{id}`')

   if text == 'الايدي العام':
      if not dev2_pls(m.from_user.id, m.chat.id):
        return
      if not r.get(f'customID:{Dev_Zaid}'):
        return m.reply(f'{k} الايدي العام مو معدل')
      else:
        id = r.get(f'customID:{Dev_Zaid}')
        return m.reply(f'`{id}`')

   if text == 'تغيير الايدي':
      if not mod_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      else:
        id = random.choice(custom_ids)
        r.set(f'{m.chat.id}:customID:{Dev_Zaid}', id)
        m.reply(f'{k} وسوينا الايدي\n{k} يمديك تجرب شكل الايدي الجديد الحين')

   if text == 'تعيين الايدي':
      if not mod_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

- الاختصارات:

{الاسم} ↼ يطلع اسم الشخص
{الايدي} ↼ يطلع ايدي الشخص
{اليوزر} ↼ يطلع يوزر الشخص
{الرتبه} ↼ يطلع رتبته الشخص
{التفاعل} ↼ يطلع تفاعل الشخص
{الرسائل} ↼ يطلع كم رسالة عند الشخص
{التعديل} ↼ يطلع كم مره عدل الشخص
{البايو} ↼ يطلع البايو اللي كاتبه
{تعليق} ↼ يطلع تعليق عشوائي
{الانشاء} ↼ يطلع انشاء الحساب

قناة اشكال الايدي https://t.me/eeeCASH/187

'''
      m.reply(reply)
      r.set(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_Zaid}', 1)
      return
   if text == 'تعيين الايدي عام':
      if not dev2_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} عذراً الامر يخص ↤〖 Dev²🎖 〗فقط .')
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

- الاختصارات:

{الاسم} ↼ يطلع اسم الشخص
{الايدي} ↼ يطلع ايدي الشخص
{اليوزر} ↼ يطلع يوزر الشخص
{الرتبه} ↼ يطلع رتبته الشخص
{التفاعل} ↼ يطلع تفاعل الشخص
{الرسائل} ↼ يطلع كم رسالة عند الشخص
{التعديل} ↼ يطلع كم مره عدل الشخص
{البايو} ↼ يطلع البايو اللي كاتبه
{تعليق} ↼ يطلع تعليق عشوائي
{الانشاء} ↼ يطلع انشاء الحساب

قناة اشكال الايدي https://t.me/eeeCASH/187
'''
      m.reply(reply)
      r.set(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_Zaid}', 1)
      return True


   if text == 'تفعيل الايدي':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{m.chat.id}:disableID:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} الايدي مفعل من قبل')
       else:
         r.delete(f'{m.chat.id}:disableID:{Dev_Zaid}')
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر فعلت الايدي')

   if text == 'تعطيل الايدي':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{m.chat.id}:disableID:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} الايدي معطل من قبل')
       else:
         r.set(f'{m.chat.id}:disableID:{Dev_Zaid}',1)
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر عطلت الايدي')

   if text == 'تفعيل افتاري':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{m.chat.id}:disableAV:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} افتار مفعل من قبل')
       else:
         r.delete(f'{m.chat.id}:disableAV:{Dev_Zaid}')
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر فعلت افتار')

   if text == 'تعطيل افتاري':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{m.chat.id}:disableAV:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} افتار معطل من قبل')
       else:
         r.set(f'{m.chat.id}:disableAV:{Dev_Zaid}',1)
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر عطلت افتار')

   if text == 'تعطيل الايدي بالصوره':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} الايدي بالصوره معطل من قبل')
       else:
         r.set(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}',1)
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر عطلت الايدي بالصوره')

   if text == 'تفعيل الايدي بالصوره':
     if not admin_pls(m.from_user.id,m.chat.id):
       return m.reply(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}'):
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} الايدي بالصوره مفعل من قبل')
       else:
         r.delete(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}')
         return m.reply(f'{k} بواسطة ↤ {m.from_user.mention}\n{k} ابشر فعلت الايدي بالصوره')

   if text == "لقبي":
     title = m.chat.get_member(m.from_user.id).custom_title
     if not title:
       return m.reply(f"{k} ماعندك لقب")
     else:
       return m.reply(f"{k} لقبك ↢ ( {title} )")

   if text in ['ايدي', 'ا', 'id'] and m.reply_to_message and m.reply_to_message.from_user:
       if not pre_pls(m.from_user.id, m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المميز وفوق ) بس')
       return m.reply(f'الايدي ↢ ( `{m.reply_to_message.from_user.id}` )')

   if text in ['ايدي', 'ا', 'id'] and not m.reply_to_message:
       if not pre_pls(m.from_user.id, m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المميز وفوق ) بس')
       if r.get(f'{m.chat.id}:disableID:{Dev_Zaid}'): return m.reply(f'{k} عذراً الايدي مغلق')
       if r.get(f'{m.chat.id}:customID:{Dev_Zaid}'):
         id = r.get(f'{m.chat.id}:customID:{Dev_Zaid}')
       else:
         if r.get(f'customID:{Dev_Zaid}'):
           id = r.get(f'customID:{Dev_Zaid}')
         else:
           id = '''
𖡋 𝐔𝐒𝐄 ⌯  {اليوزر}
𖡋 𝐌𝐒𝐆 ⌯  {الرسائل}
𖡋 𝐒𝐓𝐀 ⌯  {الرتبه}
𖡋 𝐈𝐃 ⌯  {الايدي}
𖡋 𝐄𝐃𝐈𝐓 ⌯  {التعديل}
𖡋 𝐂𝐑  ⌯  {الانشاء}
{البايو}'''
       if getattr(m.from_user, "usernames", None):
          username = ''
          for i in m.from_user.usernames: username += f"@{i.username} "
       elif m.from_user.username:
          username = f'@{m.from_user.username}'
       else:
          username = 'مافي يوزر'
       rank = get_rank(m.from_user.id, m.chat.id)
       msg = int(r.get(f'{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}'))
       msgs = f"{msg}"
       iD = f'`{m.from_user.id}`'
       if not r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'):
          edits = 0
       else:
          edit= int(r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_Zaid}'))
          edits = f"{edit}"
       name = m.from_user.first_name
       create = get_creation_date(m.from_user.id)
       get_chat = c.get_chat(m.from_user.id)
       if get_chat.bio :
          bio = get_chat.bio
       else:
          bio = 'مافي بايو'
       if msg > 50:
        tfa3l = 'شد حيلك'
       if msg > 500:
        tfa3l = 'يجي منك'
       if msg > 750:
        tfa3l = 'تفاعل متوسط'
       if msg > 2500:
        tfa3l = 'متفاعل'
       if msg > 5000:
        tfa3l = 'اسطورة التفاعل'
       if msg > 10000:
        tfa3l = 'اسطورة التلي'
       else:
        tfa3l = 'تفاعل صفر'
       comment = random.choice(comments)
       text = id.replace('{الاسم}', name).replace('{اليوزر}', username).replace('{الرسائل}',str(msgs)).replace('{التعديل}', str(edits)).replace('{الانشاء}', create).replace('{البايو}', f'{bio}').replace('{الايدي}', iD).replace('{الرتبه}', rank).replace('{التفاعل}', tfa3l).replace('{تعليق}', comment)
       if r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_Zaid}'):
          return m.reply(text, disable_web_page_preview=True)
       else:
          if m.from_user.photo:
           get_user = c.invoke(GetFullUser(id=(c.resolve_peer(m.from_user.id))))
           photo = get_user.full_user.profile_photo
           video = photo.video_sizes
           if video:
             if len(video) == 3:
               video = video[-2]
             else:
               video = video[-1]
           if video:
              file = BytesIO()
              hash = photo.access_hash
              if r.get(f"{hash}:{m.from_user.id}"):
                return m.reply_animation(r.get(f"{hash}:{m.from_user.id}"), caption=text)
              for byte in c.stream_media(
                message=FileId(
                  file_type=FileType.PHOTO,
                  dc_id=photo.dc_id, media_id=photo.id,
                  access_hash=photo.access_hash,
                  file_reference=photo.file_reference,
                  thumbnail_source=ThumbnailSource.THUMBNAIL,
                  thumbnail_file_type=FileType.PHOTO,
                  thumbnail_size=video.type,
                  volume_id=0, local_id=0
                ).encode()
              ):
                file.write(byte)
              file.name = f'{m.from_user.id}vid{m.chat.id}.mp4'
              send = m.reply_animation(file, caption=text)
              r.set(f"{hash}:{m.from_user.id}",send.animation.file_id,ex=3600)
              return True
           else:
              file_id=FileId(
                        file_type=FileType.PHOTO,
                        dc_id=photo.dc_id,
                        media_id=photo.id,
                        access_hash=photo.access_hash,
                        file_reference=photo.file_reference,
                        thumbnail_source=ThumbnailSource.THUMBNAIL,
                        thumbnail_file_type=FileType.PHOTO,
                        thumbnail_size=photo.sizes[0].type,
                        volume_id=0,
                        local_id=0
                    ).encode()
              return m.reply_photo(file_id, caption=text)
          else:
           return m.reply(text, disable_web_page_preview=True)


@Client.on_message(filters.new_chat_members, group=1)
def addContact(c,m):
  if not getattr(m, 'from_user', None): return
  for me in m.new_chat_members:
    if not m.from_user.id == me.id:
      if not r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'):
        r.set(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}',1)
      else:
        co = int(r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}'))
        r.set(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_Zaid}',co+1)


'''

@Client.on_message(filters.text & filters.group, group=17)
def setIDHandler(c,m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f'{Dev_Zaid}:botkey')
    set_id(c,m,k)


def set_id(c,m,k):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return
   text = m.text
   if r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')

'''



