'''


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/W_WT1"}

'''

import random, re, time
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from .all import list_UwU
from helpers.Ranks import *
from helpers.quran import *
from helpers.memes import *
from pyrogram.raw.functions.users import GetFullUser
from io import BytesIO
from pyrogram.file_id import FileId, FileType, ThumbnailSource

###########################################################################
###########################################################################
'''
@Client.on_raw_update(group=0)
def kick_from_group(app: Client, m: Update, _, __):
   if not getattr(m, 'from_user', None): return
   try:
      name = re.search(r"first_name='([^']+)'", str(_)).group(1)
      title = re.search(r"title='([^']+)'", str(__)).group(1)
      get = app.get_me()
      if 'types.ChannelParticipantBanned' in str(m) and '"is_self": true' in str(m):
        r.delete(f'{m.chat.id}:enable:{Dev_Zaid}', int(f'-100{m.channel_id}'))
        r.srem(f'enablelist:{Dev_Zaid}', int(f'-100{m.channel_id}'))
      else:
        return False
      text = '{k} تم طرد البوت من مجموعة:\n\n'
      text += f'{k} اسم الي طردني : [{name}](tg://user?id={m.new_participant.kicked_by})\n'
      text += f'{k} ايدي الي طردني : {m.new_participant.kicked_by}\n'
      text += f'\n{k} معلومات المجموعة: \n'
      text += f'\n{k} ايدي المجموعة: `-100{m.channel_id}`'
      text += f'\n{k} اسم المجموعه: {title}'
      text += '\n{k} تم مسح جميع بيانات المجموعة'
      text += '\n\n༄'
      if r.get(f'DevGroup:{Dev_Zaid}'):
        app.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
      else:
        for dev in get_devs_br():
          try:
            app.send_message(int(dev), text, disable_web_page_preview=True)
            time.sleep(3)
          except:
            pass
   except Exception as e:
     print (e)
''' 
## الردود
@Client.on_message(filters.text & filters.group, group=1)
def globalHandler(c,m):
   if not getattr(m, 'from_user', None): return
   Thread(target=global_filter,args=(c,m)).start()

def global_filter(c,m):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return 
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:lock_global:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addFilter2GG:{m.from_user.id}{Dev_Zaid}'):  return 
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{text}:filter:{Dev_Zaid}'):
     get = r.get(f'{text}:filter:{Dev_Zaid}')
     type = re.search(r'type=([^&]+)', get).group(1)
     userID = str(m.from_user.id)
     userNAME = str(m.from_user.first_name)
     userUSERNAME = "@"+m.from_user.username if m.from_user.username else "مافي يوزر"
     userMENTION = m.from_user.mention(userNAME[:25])
     if type == 'text':
        return m.reply(get.split('&text=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     
     if type == 'photo':
        photo = re.search(r'photo=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_photo(photo, caption=cpt)
     
     if type == 'video':
        video = re.search(r'video=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_video(video, caption=cpt)
     
     if type == 'voice':
        voice = re.search(r'voice=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_voice(voice, caption=cpt)
     
     if type == 'animation':
        animation = re.search(r'animation=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_animation(animation, caption=cpt)
     
     if type == 'audio':
        audio = re.search(r'audio=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_audio(audio, caption=cpt)
     
     if type == 'doc':
        doc = re.search(r'doc=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return m.reply_document(doc, caption=cpt)

     if type == 'sticker':
        return m.reply_sticker(get.split('&sticker=')[1])
   
   
   
   if text == 'المطور':
     id = int(r.get(f'{Dev_Zaid}botowner'))
     get = c.get_chat(id)
     if not get.bio:
       bio = None
     else:
       bio = get.bio
     reply_markup= InlineKeyboardMarkup (
       [[InlineKeyboardButton (get.first_name, user_id=id)]]
     )
     if not get.photo:
       return m.reply_animation('https://telegra.ph/file/d9127c65922817d127f04.mp4',caption=bio,reply_markup=reply_markup)
     else:
       get_user = c.invoke(GetFullUser(id=(c.resolve_peer(id))))
       photo = get_user.full_user.profile_photo
       video = photo.video_sizes[0] if photo.video_sizes else None
       if video:
         file = BytesIO()
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
           file.name = f'{id}vid.mp4'
           return m.reply_animation(file, caption=bio,reply_markup=reply_markup)
       else:
         for photo in c.get_chat_photos(id, limit=1):
           return m.reply_photo(photo.file_id, caption=bio, reply_markup=reply_markup)
        
        
        
@Client.on_message(filters.text & filters.group, group=2)
def filtersHandler(c,m):
   if not getattr(m, 'from_user', None): return
   
   Thread(target=get_filter,args=(c,m)).start()

def get_filter(c,m):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return 
   if r.get(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')

   # Check member filters (اضف ردي) BEFORE lock_filter so they work independently
   if r.get(f'{text}:filterMEM:{Dev_Zaid}{m.chat.id}') and not r.get(f'{m.chat.id}:lock_filterMEM:{Dev_Zaid}'):
     try:
       id = int(r.get(f'{text}:filterMEM:{Dev_Zaid}{m.chat.id}'))
       get = c.get_chat(id)
       cap = f"𖡋 𝐍𝐀𝐌𝐄 ⌯ [{get.first_name}](tg://user?id={get.id})\n𖡋 𝐈𝐃 ⌯ `{get.id}`"
       if not get.bio:
         pass
       else:
         cap+=f"\n`{get.bio}`"
       if get.username:
         reply_markup= InlineKeyboardMarkup (
         [[InlineKeyboardButton (get.first_name, user_id=id)]]
         )
       else:
         reply_markup=None
       if not get.photo:
         return m.reply(cap,reply_markup=reply_markup)
       else:
         try:
           get_user = c.invoke(GetFullUser(id=(c.resolve_peer(id))))
           photo = get_user.full_user.profile_photo
           hash = photo.access_hash
           if r.get(f"{hash}:{id}"):
             return m.reply_animation(r.get(f"{hash}:{id}"), caption=cap, reply_markup=reply_markup) 
           video = photo.video_sizes[0] if photo.video_sizes else None
           if video:
             file = BytesIO()
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
             file.name = f'{id}vid.mp4'
             a= m.reply_animation(file, caption=cap,reply_markup=reply_markup)
             return r.set(f"{hash}:{id}", a.animation.file_id, ex=120)
         except Exception as e:
           pass
         
         for photo in c.get_chat_photos(id, limit=1):
           return m.reply_photo(photo.file_id, caption=cap, reply_markup=reply_markup)
     except Exception as e:
       pass
     return

   if r.get(f'{m.chat.id}:lock_filter:{Dev_Zaid}'):  return 
   
   if r.get(f'{text}:filter:{Dev_Zaid}{m.chat.id}'):
     get = r.get(f'{text}:filter:{Dev_Zaid}{m.chat.id}')
     type = re.search(r'type=([^&]+)', get).group(1)
     userID = str(m.from_user.id)
     userNAME = str(m.from_user.first_name)
     userUSERNAME = "@"+m.from_user.username if m.from_user.username else "مافي يوزر"
     userMENTION = m.from_user.mention(userNAME[:25])
     if type == 'text':
         m.reply(get.split('&text=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     
     if type == 'photo':
        photo = re.search(r'photo=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_photo(photo, caption=cpt)
     
     if type == 'video':
        video = re.search(r'video=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_video(video, caption=cpt)
     
     if type == 'voice':
        voice = re.search(r'voice=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_voice(voice, caption=cpt)
     
     if type == 'animation':
        animation = re.search(r'animation=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_animation(animation, caption=cpt)
     
     if type == 'audio':
        audio = re.search(r'audio=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_audio(audio, caption=cpt)
    
     if type == 'doc':
        doc = re.search(r'doc=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        m.reply_document(doc, caption=cpt)

     if type == 'sticker':
         m.reply_sticker(get.split('&sticker=')[1])
        
      



@Client.on_message(filters.text & filters.group, group=3)
def globalRandomupdate(c,m):
   if not getattr(m, 'from_user', None): return
   Thread(target=get_rngp,args=(c,m)).start()
   
def get_rngp(c,m):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
   if r.get(f'{m.chat.id}:lock_global:{Dev_Zaid}'):  return 
   
   if m.from_user:
     if r.get(f'{m.chat.id}:addFilterRG:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:delFilterRG:{m.from_user.id}{Dev_Zaid}'):  return 
     if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
     if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   userID = str(m.from_user.id)
   userNAME = str(m.from_user.first_name)
   userUSERNAME = "@"+m.from_user.username if m.from_user.username else "مافي يوزر"
   userMENTION = m.from_user.mention(userNAME[:25])
   if r.get(f'{text}:randomFilter:{Dev_Zaid}'):
     if r.smembers(f'{text}:randomfilter:{Dev_Zaid}'):
        items = tuple(r.smembers(f'{text}:randomfilter:{Dev_Zaid}'))
        return m.reply(random.choice(items).replace('{اسم_البوت}',name).replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
   name2 = ' '.join(i for i in name)
   
   
   sb = [
"عييييييييب","عيب","ياكلب عيب","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟","استغفر الله",
   ]
   lovem = [
"يلبيييه",
"اكثر",
"يعمري",
"اعشقك",
"بدينا كذب",
"احلى من يحبني",
"يحظي والله",
"اكثر اكثر اكثرر",
"يروحي",
"اموت فيك",]
   zg = [
"عييييييييب","عيب","زق بوجهك","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟",]
   mm = [
"ابركها من ساعة","احبك","اكثر","ترا ازعجتنا","انقلع","طيب","مو اكثر مني","وبعدين ؟","جت من الله","توكل بس"]
   bot_r = ["شكد غبي انت اسمي اتاك مو بوت 😡", "لك اسمي اتاك شبيك تصيحلي بوت 😤", "اسمي اتاك يا ثول مو بوت 😒", "لا تكولي بوت اسمي اتاك خوش؟ 😠", "احترم نفسك وسميني اتاك مو بوت 🤬"]
   bot_name = ["يا عيون اتاك انت 😍", "فديت الي يصيحلي اتاك 🥰", "روح اتاك وقلبه تفضل حبيبي 😘", "يا بعد عمري نعم تفضل 🥰", "يوه فديتك تدلل شتريد؟ 💕"]
   if text == 'بوت':
      m.reply(random.choice(bot_r))
   
   if text == name:
     m.reply(random.choice(bot_name))
     
   '''
   if text in list_UwU:
     m.reply(random.choice(sb))
   '''
   
   if text == 'احبك':
     m.reply(random.choice(lovem))
   
   if text == 'اكرهك':
     m.reply(random.choice(mm))
   
   if text == 'كليزق' or text == 'كلزق':
     m.reply(random.choice(zg))
   
   if text.startswith('سورة ') or text.startswith('سوره '):
      soura = text.split(None,1)[1].replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٰ','').replace('ة','ه')
      if f'سورة {soura}' in TheHolyQuran:
        title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
        return m.reply_audio(
          MaherAlmaikulai[f"سورة {soura}"],
          caption=f'سورة {soura}',
          reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/eeeCASH')
            ],
            [
              InlineKeyboardButton ('بصوت سعد الغامدي',callback_data=f'{m.from_user.id}quSaad={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ],
            [
              InlineKeyboardButton ('بصوت عبد الباسط عبد الصمد',callback_data=f'{m.from_user.id}quBaset={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ],
            [
              InlineKeyboardButton ('بصوت مشاري راشد العفاسي',callback_data=f'{m.from_user.id}qu3fasy={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ]
            ]
          )
        )
   
   if text == 'ميمز':
     randomMeme = random.choice(memes_sa)
     return m.reply_audio(
     randomMeme["url"],caption=randomMeme["title"],
     reply_markup=InlineKeyboardMarkup (
       [
         [InlineKeyboardButton ('🇸🇾',callback_data=f'{m.from_user.id}memes_sy'),InlineKeyboardButton ('🇪🇬',callback_data=f'{m.from_user.id}memes_eg')],
         [InlineKeyboardButton ('🇸🇦',callback_data=f'{m.from_user.id}memes_sa'),InlineKeyboardButton ('🇦🇪',callback_data=f'{m.from_user.id}memes_ae')],
         [InlineKeyboardButton ('🇺🇸',callback_data=f'{m.from_user.id}memes_us'),InlineKeyboardButton ('🇮🇶',callback_data=f'{m.from_user.id}memes_iq'),],
         [InlineKeyboardButton ('🧚‍♀️',url='https://t.me/eeeCASH')],
       ]
     )
     )
   #https://raw.githubusercontent.com/maknon/Quran/main/pages-douri/604.png
   if (text.startswith('قرآن ') or text.startswith('قران ')) and re.findall('[0-9]+', text):
     page = int(re.findall('[0-9]+', text)[0])
     if page <= 604:
        title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
        return m.reply_photo(f'https://raw.githubusercontent.com/maknon/Quran/main/pages-douri/{page}.png',reply_markup=InlineKeyboardMarkup (
          [[
            InlineKeyboardButton (title,url='https://t.me/eeeCASH')
          ]]
        ))
       

@Client.on_callback_query(filters.regex('memes'))
def memes(c,m):
   if not getattr(m, 'from_user', None): return
   if str(m.from_user.id) in m.data:
     if m.data.endswith('sy'):
       list = memes_sy
     if m.data.endswith('eg'):
       list = memes_eg
     if m.data.endswith('sa'):
       list = memes_sa
     if m.data.endswith('ae'):
       list = memes_ae
     if m.data.endswith('us'):
       list = memes_us
     if m.data.endswith('iq'):
       list = memes_iq
     randomMeme = random.choice(list)
     try:
       return m.edit_message_media(media=InputMediaAudio(media=randomMeme["url"],caption=randomMeme["title"],),
       reply_markup=m.message.reply_markup)
     except:
       m.message.reply_to_message.reply_audio(randomMeme["url"],caption=randomMeme["title"],reply_markup=m.message.reply_markup)
       return m.message.delete()

@Client.on_callback_query(filters.regex('quSaad'))
def quSaad(c,m):
   if not getattr(m, 'from_user', None): return
   if m.data.startswith(f'{m.from_user.id}quSaad'):
      soura = m.data.split('=')[1]
      title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
      return m.edit_message_media(
        media=InputMediaAudio(
          media=f'https://t.me/SaadSounds/{soura}',
          caption=m.message.caption
        ),
        reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/eeeCASH')
            ],
            [
              InlineKeyboardButton ('بصوت ماهر المعيقلي',callback_data=f'{m.from_user.id}quMaher={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت عبد الباسط عبد الصمد',callback_data=f'{m.from_user.id}quBaset={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت مشاري راشد العفاسي',callback_data=f'{m.from_user.id}qu3fasy={soura}')
            ]
            ]
          )
        )
      

@Client.on_callback_query(filters.regex('quMaher'))
def quMaher(c,m):
   if not getattr(m, 'from_user', None): return
   if m.data.startswith(f'{m.from_user.id}quMaher'):
      soura = m.data.split('=')[1]
      title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
      return m.edit_message_media(
        media=InputMediaAudio(
          media=f'https://t.me/MaherSounds/{soura}',
          caption=m.message.caption
        ),
        reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/W_WT1')
            ],
            [
              InlineKeyboardButton ('بصوت سعد الغامدي',callback_data=f'{m.from_user.id}quSaad={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت عبد الباسط عبد الصمد',callback_data=f'{m.from_user.id}quBaset={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت مشاري راشد العفاسي',callback_data=f'{m.from_user.id}qu3fasy={soura}')
            ]
            ]
          )
        )
        
@Client.on_callback_query(filters.regex('qu3fasy'))
def qu3fasy(c,m):
   if not getattr(m, 'from_user', None): return
   if m.data.startswith(f'{m.from_user.id}qu3fasy'):
      soura = m.data.split('=')[1]
      title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
      return m.edit_message_media(
        media=InputMediaAudio(
          media=f'https://t.me/Al3afasy/{soura}',
          caption=m.message.caption
        ),
        reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/W_WT1')
            ],
            [
              InlineKeyboardButton ('بصوت سعد الغامدي',callback_data=f'{m.from_user.id}quSaad={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت عبد الباسط عبد الصمد',callback_data=f'{m.from_user.id}quBaset={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت ماهر المعيقلي',callback_data=f'{m.from_user.id}quMaher={soura}')
            ]
            ]
          )
        )
        
@Client.on_callback_query(filters.regex('quBaset'))
def quBaset(c,m):
   if not getattr(m, 'from_user', None): return
   if m.data.startswith(f'{m.from_user.id}quBaset'):
      soura = m.data.split('=')[1]
      title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
      return m.edit_message_media(
        media=InputMediaAudio(
          media=f'https://t.me/AbdAlbasetS/{soura}',
          caption=m.message.caption
        ),
        reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/W_WT1')
            ],
            [
              InlineKeyboardButton ('بصوت سعد الغامدي',callback_data=f'{m.from_user.id}quSaad={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت مشاري راشد العفاسي',callback_data=f'{m.from_user.id}qu3fasy={soura}')
            ],
            [
              InlineKeyboardButton ('بصوت ماهر المعيقلي',callback_data=f'{m.from_user.id}quMaher={soura}')
            ]
            ]
          )
        )
      
    
@Client.on_message(filters.text & filters.group, group=4)
def randomfiltersHandler(c,m):
   if not getattr(m, 'from_user', None): return
   Thread(target=get_rn_filter,args=(c,m)).start()
   
   
def get_rn_filter(c,m):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:lock_filter:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
   if m.from_user:
     if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return
     if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
     if r.get(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_Zaid}'):  return
     if r.get(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_Zaid}'):  return 
     if r.get(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_Zaid}'):  return 
     if r.get(f'{m.chat.id}:delFilterR:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:addFilterR:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:addFilterR2:{m.from_user.id}{Dev_Zaid}'):  return 
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   userID = str(m.from_user.id)
   userNAME = str(m.from_user.first_name)
   userUSERNAME = "@"+m.from_user.username if m.from_user.username else "مافي يوزر"
   userMENTION = m.from_user.mention(userNAME[:25])
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{text}:randomFilter:{m.chat.id}{Dev_Zaid}'):
       items = tuple(r.smembers(f'{text}:randomfilter:{m.chat.id}{Dev_Zaid}'))
       return m.reply(random.choice(items).replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     

@Client.on_message(filters.left_chat_member)
def kick_from_gp(c,m):
   if not getattr(m, 'from_user', None): return
   if m.left_chat_member.id == int(Dev_Zaid):
        k = r.get(f'{Dev_Zaid}:botkey')
        text = f'{k} من「 {m.from_user.mention} 」\n'
        usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{m.from_user.id}`\n'
        text += f'\n{k} قام بطرد البوت من المجموعة :\n\n'
        text += f'{k} اسم المجموعة : {m.chat.title}\n'
        chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{m.chat.id}`'
        r.srem(f'enablelist:{Dev_Zaid}', m.chat.id)
        r.delete(f'{m.chat.id}:enable:{Dev_Zaid}')
        if r.smembers(f'enablelist:{Dev_Zaid}'):
          text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += f'\n{k} تم مسح جميع بيانات المجموعة'
        text += '\n\n☆'
        if r.get(f'DevGroup:{Dev_Zaid}'):
          c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
        else:
          for dev in get_devs_br():
                 try:
                    c.send_message(int(dev), text, disable_web_page_preview=True)
                    time.sleep(3)
                 except:
                    pass

@Client.on_chat_member_updated(filters.group, group=5)
def ChatMemberUpdate(c,m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f'{Dev_Zaid}:botkey')
    get_bot_status(c,m,k)
    
def get_bot_status(c,m,k):
  if not getattr(m, 'from_user', None): return
  try:
    if m.new_chat_member.status == ChatMemberStatus.MEMBER:
       if m.new_chat_member.user.id == c.me.id:
         if r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
             text = f'{k} من「 {m.from_user.mention} 」\n'
             text += f'{k} تم تعطيل المجموعة تلقائياً\n☆'
             c.send_message(m.chat.id, text)
             text = f'{k} من「 {m.from_user.mention} 」\n'
             usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
             text += f'{k} يوزره : {usrr}\n'
             text += f'{k} ايديه : `{m.from_user.id}`\n'
             text += f'\n{k} قام بتنزيل البوت من الأدمن :\n\n'
             text += f'{k} اسم المجموعة : {m.chat.title}\n'
             chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
             text += f'{k} يوزر المجموعة : {chatusr}\n'
             text += f'{k} ايدي المجموعة : `{m.chat.id}`'             
             r.srem(f'enablelist:{Dev_Zaid}', m.chat.id)
             r.delete(f'{m.chat.id}:enable:{Dev_Zaid}')
             if r.smembers(f'enablelist:{Dev_Zaid}'):
               text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
             text += f'\n{k} تم مسح جميع بيانات المجموعة'
             text += '\n\n☆'
             if r.get(f'DevGroup:{Dev_Zaid}'):
                   c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
             else:
               for dev in get_devs_br():
                 try:
                    c.send_message(int(dev), text, disable_web_page_preview=True)
                    time.sleep(3)
                 except:
                    pass
              
                
    if m.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
       if m.new_chat_member.user.id == c.me.id:
          if r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
             priv = m.new_chat_member.privileges
             if not priv.can_manage_chat or not priv.can_delete_messages or not priv.can_restrict_members or not priv.can_pin_messages or not priv.can_invite_users:
                text = f'{k} من「 {m.from_user.mention} 」\n'
                text += f'{k} تم تعطيل المجموعة تلقائياً\n☆'
                c.send_message(m.chat.id, text)
                r.delete(f'{m.chat.id}:enable:{Dev_Zaid}')
                text = f'{k} من「 {m.from_user.mention} 」\n'
                usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{m.from_user.id}`\n'
                text += f'\n{k} قام بتعديل صلاحية البوت بمجموعة :\n\n'
                text += f'{k} اسم المجموعة : {m.chat.title}\n'
                chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                if r.smembers(f'enablelist:{Dev_Zaid}'):
                  text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
                text += f'\n{k} تم مسح جميع بيانات المجموعة'
                text += '\n\n☆'
                if r.get(f'DevGroup:{Dev_Zaid}'):
                   c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
                else:
                  for dev in get_devs_br():
                    try:
                      c.send_message(int(dev), text, disable_web_page_preview=True)
                      time.sleep(3)
                    except:
                      pass
                return True
                
          if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
             if r.get(f'DisableBot:{Dev_Zaid}'):
               return c.send_message(m.chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')
             priv = m.new_chat_member.privileges
             if priv.can_manage_chat and priv.can_delete_messages and priv.can_restrict_members and priv.can_pin_messages and priv.can_invite_users:
                text = f'{k} من「 {m.from_user.mention} 」\n'
                text += f'{k} تم تفعيل المجموعة تلقائياً\n☆'
                c.send_message(m.chat.id, text, reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('Commands', url=f'https://t.me/{botUsername}?start=Commands')]]))
                r.set(f'{m.chat.id}:enable:{Dev_Zaid}', 1)
                r.sadd(f'enablelist:{Dev_Zaid}', m.chat.id)
                r.set(f'{m.chat.id}:rankOWNER:{m.from_user.id}{Dev_Zaid}', 1)
                r.sadd(f'{m.chat.id}:listOWNER:{Dev_Zaid}', m.from_user.id)
                for member in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
                   if not member.user.is_bot and not member.user.is_deleted:
                      if member.status == ChatMemberStatus.OWNER:
                         r.set(f'{m.chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}', 1)
                         r.sadd(f'{m.chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
                         r.sadd(f'{member.user.id}:groups', m.chat.id)
                      if member.status == ChatMemberStatus.ADMINISTRATOR:
                         r.set(f'{m.chat.id}:rankADMIN:{member.user.id}{Dev_Zaid}', 1)
                         r.sadd(f'{m.chat.id}:listADMIN:{Dev_Zaid}', member.user.id)
                get = c.get_chat(m.chat.id)
                text = f'{k} من「 {m.from_user.mention} 」\n'
                usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{m.from_user.id}`\n'
                text += f'\n{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
                text += f'{k} اسم المجموعة : {m.chat.title}\n'
                chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                if get.invite_link:
                  reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (m.chat.title,url=get.invite_link)]])
                else:
                  reply_markup=None
                if r.smembers(f'enablelist:{Dev_Zaid}'):
                   text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
                text += '\n\n☆'
                if r.get(f'DevGroup:{Dev_Zaid}'):
                   c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,reply_markup=reply_markup,disable_web_page_preview=True)
                else:
                  for dev in get_devs_br():
                    try:
                      c.send_message(int(dev), text, disable_web_page_preview=True,reply_markup=reply_markup)  
                      time.sleep(3)
                    except:
                      pass
  except:
    pass
    
                

    
    
@Client.on_message(filters.text & filters.group, group=6)
async def EnableAndDisablegroup(c,m):
  if not getattr(m, 'from_user', None): return
  text = m.text
  k = r.get(f'{Dev_Zaid}:botkey')
  if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
  if text == 'تفعيل':
    if not (await m.chat.get_member(m.from_user.id)).status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and not owner_pls(m.from_user.id,m.chat.id):
       return await m.reply(f'ادري حلم الاعضاء تفعيل البوتات بس اسف')
    if r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return await m.reply(f'{k} المجموعة مفعلة من قبل يالطيب')
    if r.get(f'DisableBot:{Dev_Zaid}'):
       return await c.send_message(m.chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')
    get = await c.get_chat_member(m.chat.id, c.me.id)
    priv = get.privileges
    if not priv.can_manage_chat or not priv.can_delete_messages or not priv.can_pin_messages or not priv.can_invite_users:
      return await m.reply(f'{k} عطيني كل الصلاحيات بعدين ارسل تفعيل')
    else:
        r.set(f'{m.chat.id}:enable:{Dev_Zaid}', 1)
        r.sadd(f'enablelist:{Dev_Zaid}', m.chat.id)
        r.set(f'{m.chat.id}:rankOWNER:{m.from_user.id}{Dev_Zaid}', 1)
        r.sadd(f'{m.chat.id}:listOWNER:{Dev_Zaid}', m.from_user.id)
        await m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر تم تفعيل المجموعة ورفعت كل الادمن\n☆', reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('Commands', url=f'https://t.me/{botUsername}?start=Commands')]]))
        async for member in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
          if not member.user.is_bot and not member.user.is_deleted:
            if member.status == ChatMemberStatus.OWNER:
              r.set(f'{m.chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}', 1)
              r.sadd(f'{m.chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
              r.sadd(f'{member.user.id}:groups',m.chat.id)
            if member.status == ChatMemberStatus.ADMINISTRATOR:
              r.set(f'{m.chat.id}:rankADMIN:{member.user.id}{Dev_Zaid}', 1)
              r.sadd(f'{m.chat.id}:listADMIN:{Dev_Zaid}', member.user.id)
        get = await c.get_chat(m.chat.id)
        text = f'{k} من「 {m.from_user.mention} 」\n'
        usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{m.from_user.id}`\n'
        text += f'\n{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
        text += f'{k} اسم المجموعة : {m.chat.title}\n'
        chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{m.chat.id}`'
        if r.smembers(f'enablelist:{Dev_Zaid}'):
           text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += '\n\n☆'
        if get.invite_link:
           reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (m.chat.title,url=get.invite_link)]])
        else:
           reply_markup=None
        if r.get(f'DevGroup:{Dev_Zaid}'):
                   await c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,reply_markup=reply_markup,disable_web_page_preview=True)
        else:
               for dev in get_devs_br():
                 try:
                    await c.send_message(int(dev), text, disable_web_page_preview=True,reply_markup=reply_markup)
                    time.sleep(3)
                 except:
                    pass
  
  if text == 'تعطيل':
    if not (await m.chat.get_member(m.from_user.id)).status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and not owner_pls(m.from_user.id,m.chat.id):
       return await m.reply('ادري حلم الاعضاء تعطيل البوتات بس اسف')
    else:
      if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return False
      else:
        r.delete(f'{m.chat.id}:enable:{Dev_Zaid}', 1)
        r.srem(f'enablelist:{Dev_Zaid}', m.chat.id)
        await m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} تم تعطيل المجموعة\n☆')
        text = f'{k} من「 {m.from_user.mention} 」\n'
        usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{m.from_user.id}`\n'
        text += f'\n{k} تم تعطيل البوت بمجموعة جديدة :\n\n'
        text += f'{k} اسم المجموعة : {m.chat.title}\n'
        chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{m.chat.id}`'
        if r.smembers(f'enablelist:{Dev_Zaid}'):
           text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += '\n\n☆'
        if r.get(f'DevGroup:{Dev_Zaid}'):
                   await c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
        else:
               for dev in get_devs_br():
                 try:
                    await c.send_message(int(dev), text, disable_web_page_preview=True)
                    time.sleep(3)
                 except:
                    pass
  
  name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
  if text == f'{name} اطلعي' or text == f'{name} اطلع':
    leave_vids = [
  {'vid':'https://t.me/D7BotResources/154','caption':'غدرتو فيني'},
  {'vid':'https://t.me/D7BotResources/155','caption':':('},
  {'vid':'https://t.me/D7BotResources/156','caption':'يلا خلي البوتات الثانيه تدلعكم'},
  {'vid':'https://t.me/D7BotResources/157','caption':'اسف لي'},
  {'vid':'https://t.me/D7BotResources/158','caption':'قلي منهو لجل عينه تغيرت'},
  {'vid':'https://t.me/D7BotResources/159','caption':'واخيرا برتاح منكم يا نشبه العمر'},]
    if owner_pls(m.from_user.id,m.chat.id):
      r.delete(f'{m.chat.id}:enable:{Dev_Zaid}', 1)
      r.srem(f'enablelist:{Dev_Zaid}', m.chat.id)
      vid = random.choice(leave_vids)
      await m.reply_video(vid['vid'], caption=vid['caption'])
      text = f'{k} من「 {m.from_user.mention} 」\n'
      usrr = '@'+m.from_user.username if m.from_user.username else 'مافيه'
      text += f'{k} يوزره : {usrr}\n'
      text += f'{k} ايديه : `{m.from_user.id}`\n'
      text += f'\n{k} طلعت من المجموعة بأمر منه :\n\n'
      text += f'{k} اسم المجموعة : {m.chat.title}\n'
      chatusr = '@'+m.chat.username if m.chat.username else 'مافيه'
      text += f'{k} يوزر المجموعة : {chatusr}\n'
      text += f'{k} ايدي المجموعة : `{m.chat.id}`'
      if r.smembers(f'enablelist:{Dev_Zaid}'):
        text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
      text += '\n\n☆'
      await c.leave_chat(m.chat.id)
      if r.get(f'DevGroup:{Dev_Zaid}'):
        await c.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
      else:
        for dev in get_devs_br():
          try:
            await c.send_message(int(dev), text, disable_web_page_preview=True)
          except:
            pass
      
@Client.on_chat_member_updated(filters.group, group=8)
def anti_raid_protection(c, m):
    if not getattr(m, 'from_user', None): return
    if not m.from_user or not m.new_chat_member: return
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'): return
    
    # Check if user was banned or kicked (ChatMemberStatus.BANNED)
    if m.new_chat_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
        admin_id = m.from_user.id
        
        # Prevent acting on self or main devs
        if admin_id == c.me.id: return
        if str(admin_id) in get_devs_br() or admin_id == owner_id: return
        
        # Prevent acting on the REAL Telegram Group Creator
        try:
            admin_member = c.get_chat_member(m.chat.id, admin_id)
            if admin_member.status == ChatMemberStatus.OWNER:
                return
        except Exception:
            pass
            
        # Count kicks in 60 seconds window (7 kicks = raid)
        key = f'{Dev_Zaid}:anti_raid:{m.chat.id}:{admin_id}'
        count = r.incr(key)
        if count == 1:
            r.expire(key, 60) 
            
        if count >= 7:
            r.delete(key) # Prevent spamming the alert
            
            # Try finding the group owner for mention
            owner_mentions = ""
            owner_list = r.smembers(f'{m.chat.id}:listGOWNER:{Dev_Zaid}')
            if owner_list:
                for o in owner_list:
                    owner_mentions += f"[{int(o)}](tg://user?id={int(o)}) "
            else:
                for member in c.get_chat_members(m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
                    if member.status == ChatMemberStatus.OWNER:
                        owner_mentions += member.user.mention
                        break
            
            demoted = False
            try:
                # Demote the admin completely
                c.promote_chat_member(
                    m.chat.id, 
                    admin_id,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_promote_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        is_anonymous=False
                    )
                )
                demoted = True
            except Exception as e:
                pass
                
            msg = f"⚠️ **تحذير أمني! محاولة تخريب (تفليش)!**\n\n"
            msg += f"المشرف {m.from_user.mention} قام بطرد عدد كبير من الأعضاء في وقت قصير جداً.\n"
            if demoted:
                msg += f"✅ تم تنزيله من الإشراف تلقائياً لحماية المجموعة.\n"
            else:
                msg += f"❌ فشل البوت في تنزيله من الإشراف (ليس لدي صلاحية كافية لتنزيله أو أنه منشئ).\n"
                
            if owner_mentions:
                msg += f"\nمالك المجموعة: {owner_mentions} يرجى التدخل فوراً!"
                
            try:
                c.send_message(m.chat.id, msg)
            except:
                pass
