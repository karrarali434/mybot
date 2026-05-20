'''


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/GGGGG1S"}

'''

import random, re, time
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand


@Client.on_message(filters.text & filters.group, group=7)
def ranksCommandsHandler(c,m):
   if not getattr(m, 'from_user', None): return
   k = r.get(f'{Dev_Zaid}:botkey')
   Thread(target=ranks_reply_promote,args=(c,m,k)).start()
   

def ranks_reply_promote(c,m,k):
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
    if text == 'تعطيل الرفع':
      if not owner_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if r.get(f'{m.chat.id}:disableRanks:{Dev_Zaid}'):
          return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} الرفع معطل من قبل\n☆')
        else:
          r.set(f'{m.chat.id}:disableRanks:{Dev_Zaid}', 1)
          return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت الرفع\n☆')
    
    if text == 'تفعيل الرفع':
      if not owner_pls(m.from_user.id, m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if not r.get(f'{m.chat.id}:disableRanks:{Dev_Zaid}'):
          return m.reply(f'「 {m.from_user.mention} 」\n{k} الرفع مفعل من قبل\n☆')
        else:
          r.delete(f'{m.chat.id}:disableRanks:{Dev_Zaid}')
          return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت الرفع\n☆')
    
    cid = m.chat.id
    
    if r.get(f'{m.chat.id}:disableRanks:{Dev_Zaid}'): return m.reply(f'{k} عذراً نظام الرتب مغلق')
    rank = get_rank(m.from_user.id, m.chat.id)
    if text.startswith('رفع Dev ') or text.startswith('مط '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not devp_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        
           
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} Dev²🎖 من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV2:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV2', id)
          return m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Dev²🎖\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع Dev', 'مط'] and m.reply_to_message and m.reply_to_message.from_user:
        if not devp_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')           
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} Dev²🎖 من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV2:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV2', id)
          return m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Dev²🎖\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          
    if text.startswith('رفع MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return False
        if not dev2_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} Myth🎖️ من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Myth🎖️\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع MY' and m.reply_to_message and m.reply_to_message.from_user:
        if not dev2_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} Myth🎖️ من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Myth🎖️\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    cid = m.chat.id
    
    if text.startswith('رفع منشئ اساسي ') or text.startswith('اس '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} منشئ اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankGOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ اساسي\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          return 
    
    if text in ['رفع منشئ اساسي', 'اس'] and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention       
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} منشئ اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankGOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ اساسي\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          return 
    

    if text.startswith('رفع منشئ ') or text.startswith('من '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        
        sender_rank = rank
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} منشئ من قبل\n☆')
        else:
          r.set(f'{cid}:rankCREATOR:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع منشئ', 'من'] and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        sender_rank = rank
        rank = get_rank(id, cid)
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} منشئ من قبل\n☆')
        else:
          r.set(f'{cid}:rankCREATOR:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)

    if text.startswith('رفع مالك ') or text.startswith('ما '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مالك من قبل\n☆')
        else:
          r.set(f'{cid}:rankOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listOWNER:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع مالك', 'ما'] and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مالك من قبل\n☆')
        else:
          r.set(f'{cid}:rankOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listOWNER:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    
    if text.startswith('رفع مدير ') or text.startswith('مد '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not owner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مدير من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOD:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOD:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مدير\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع مدير', 'مد'] and m.reply_to_message and m.reply_to_message.from_user:
        if not owner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مدير من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOD:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOD:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مدير\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text.startswith('رفع ادمن ') or text.startswith('اد '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not mod_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
           
        if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} ادمن من قبل\n☆')
        else:
          r.set(f'{cid}:rankADMIN:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listADMIN:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار ادمن\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع ادمن', 'اد'] and m.reply_to_message and m.reply_to_message.from_user:        
        if not mod_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
           
        if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} ادمن من قبل\n☆')
        else:
          r.set(f'{cid}:rankADMIN:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listADMIN:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار ادمن\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text.startswith('رفع مميز ') or text.startswith('م '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not admin_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مميز من قبل\n☆')
        else:
          r.set(f'{cid}:rankPRE:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listPRE:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مميز\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع مميز', 'م'] and m.reply_to_message and m.reply_to_message.from_user:
      if not admin_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف ارفع نفسي')
        if id == m.from_user.id:
           return m.reply(f'{k} هطف تبي ترفع نفسك؟')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مميز من قبل\n☆')
        else:
          r.set(f'{cid}:rankPRE:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listPRE:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مميز\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          
    
    
    
@Client.on_message(filters.text & filters.group, group=8)
def ranksCommandsHandlerDemote(c,m):
   if not getattr(m, 'from_user', None): return
   k = r.get(f'{Dev_Zaid}:botkey')
   ranks_reply_demote(c,m,k)


def ranks_reply_demote(c,m,k):
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
    rank = get_rank(m.from_user.id, m.chat.id)
    cid = m.chat.id
    
    if text == 'تك' and m.reply_to_message and m.reply_to_message.from_user:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        
        if id == int(Dev_Zaid):
            return m.reply('ركز حبيبي كيف انزل المبرمج')
        if id == m.from_user.id:
            return m.reply(f'{k} هطف تبي تنزل نفسك؟')
            
        target_rank_str = get_rank(id, cid)
        
        if target_rank_str == 'عضو':
            return m.reply(f'「 {mention} 」\n{k} هو عضو من الأساس\n☆')
            
        can_demote = False
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
            if devp_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{id}:rankDEV:{Dev_Zaid}'):
            if dev2_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
            if gowner_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
            if gowner_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
            if owner_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
            if mod_pls(m.from_user.id, cid): can_demote = True
        elif r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
            if admin_pls(m.from_user.id, cid): can_demote = True
            
        if not can_demote:
            return m.reply(f'{k} رتبتك ما تسمح تنزل هذا الشخص')
            
        r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
        r.srem(f'{Dev_Zaid}DEV2', id)
        r.delete(f'{id}:rankDEV:{Dev_Zaid}')
        r.srem(f'{Dev_Zaid}DEV', id)
        r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
        
        return m.reply(f'「 {mention} 」\n{k} تم تنزيله من جميع الرتب بنجاح وصار عضو\n☆')
        
    if text == 'تنزيل Dev' and m.reply_to_message and m.reply_to_message.from_user:
        if not devp_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention     
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')           
        if not r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو Dev²🎖\n☆')
        else:
          r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV2', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من Dev²🎖\n☆')
    
    if text.startswith('تنزيل Dev '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not devp_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')           
        if not r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو Dev²🎖\n☆')
        else:
          r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV2', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من Dev²🎖\n☆')
          
    if text == 'تنزيل MY'  and m.reply_to_message and m.reply_to_message.from_user:
        if not dev2_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')           
        if not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو Myth🎖️ من قبل\n☆')
        else:
          r.delete(f'{id}:rankDEV:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من Myth🎖️\n☆')
    
    if text.startswith('تنزيل MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not dev2_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
           
        if not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو Myth🎖️ من قبل\n☆')
        else:
          r.delete(f'{id}:rankDEV:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من Myth🎖️\n☆')
    
    
    
    if text == 'تنزيل منشئ اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو منشئ اساسي\n☆')
        else:
          r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')
    
    if text.startswith('تنزيل منشئ اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو منشئ اساسي\n☆')
        else:
          r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')
    
    
    if text.startswith('تنزيل مالك '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')        
        '''
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention
        '''        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')        
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك \n☆')
    

    if text == 'تنزيل منشئ' and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو منشئ من قبل\n☆')
        else:
          r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من منشئ\n☆')
    
    if text.startswith('تنزيل منشئ '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو منشئ من قبل\n☆')
        else:
          r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من منشئ\n☆')

    if text == 'تنزيل مالك' and m.reply_to_message and m.reply_to_message.from_user:    
        
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention     
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')        
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك \n☆')

    if text.startswith('تنزيل مدير '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not owner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
           
        if not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مدير من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من رتبة المدير \n☆')
    
    if text == 'تنزيل مدير' and m.reply_to_message and m.reply_to_message.from_user:
        if not owner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        
        sender_rank = rank

        
        rank = get_rank(id, cid)

        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
           
        if not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مدير من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من رتبة المدير \n☆')
    
    if text.startswith('تنزيل ادمن '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not mod_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو ادمن من قبل\n☆')
        else:
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من رتبة الادمن \n☆')
    
    if text == 'تنزيل ادمن' and m.reply_to_message and m.reply_to_message.from_user:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو ادمن من قبل\n☆')
        else:
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من رتبة الادمن \n☆')
    
    if text.startswith('تنزيل مميز '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not admin_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
        if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مميز من قبل\n☆')
        else:
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المميزين \n☆')
    
    if text == 'تنزيل مميز' and m.reply_to_message and m.reply_to_message.from_user:
        if not admin_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        sender_rank = rank

        rank = get_rank(id, cid)

        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مميز من قبل\n☆')
        else:
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المميزين \n☆')
    
    if text.startswith('تنزيل الكل ') or text.startswith('تك '):
       if not '@' in text and not re.findall('[0-9]+', text):
          return 
       if not mod_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
       
       if len(text.split()) >= 2:
           user = text.split()[-1]
           if user.startswith('@'):
              try:
                 get = c.get_users(user.lstrip('@'))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = c.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return m.reply(f'{k} مافيه عضو بهذا الآيدي')
       
       sender_rank = rank

       
       rank = get_rank(id, cid)

       
       if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
       if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
       if devp_pls(m.from_user.id,m.chat.id):
          rank = get_rank(id,cid)
          if id == m.from_user.id:
             return m.reply(f'{k} مافيك تنزل نفسك')
          if not rank == 'عضو' and not id in [6168217372]:
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV2', id)
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887]:
              return m.reply(f'{k} مايمديك تستخدم الأمر على مبرمج السورس')
          else:
              return m.reply(f'{k} ماله رتبة')
       
       if dev2_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372]:
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')

       if dev_pls(m.from_user.id, m.chat.id):
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}'):
               m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}'):
               return m.reply(f'{k} رتبته اعلى منك')
           else:
               return m.reply(f'{k} ماله رتبة')
       
       if gowner_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')
       
       if owner_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')
       
       if mod_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')
       
       if admin_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')
    
    
    if text == 'تنزيل الكل' and m.reply_to_message and m.reply_to_message.from_user:
       if not owner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
       
       id = m.reply_to_message.from_user.id
       mention= m.reply_to_message.from_user.mention
       
       sender_rank = rank

       
       rank = get_rank(id, cid)

       
       if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
       if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
       if devp_pls(m.from_user.id,m.chat.id):
          rank = get_rank(id,cid)
          if id == m.from_user.id:
             return m.reply(f'{k} مافيك تنزل نفسك')
          if not rank == 'عضو' and not id in [6168217372]:
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV2', id)
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887]:
              return m.reply(f'{k} مايمديك تستخدم الأمر على مبرمج السورس')
          else:
             return m.reply(f'{k} ماله رتبة')
       
       if dev2_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372]:
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')
       
       if dev_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')

       if gowner_pls(m.from_user.id, m.chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
               m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}'):
               return m.reply(f'{k} رتبته اعلى منك')
           else:
               return m.reply(f'{k} ماله رتبة')
       
       if owner_pls(m.from_user.id, m.chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return m.reply(f'{k} رتبته اعلى منك')
          else:
              return m.reply(f'{k} ماله رتبة')

       if mod_pls(m.from_user.id, m.chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(
                   f'{id}:rankDEV:{Dev_Zaid}') and not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(
                   f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
               m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
               return m.reply(f'{k} رتبته اعلى منك')
           else:
               return m.reply(f'{k} ماله رتبة')

       if admin_pls(m.from_user.id, m.chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(
                   f'{id}:rankDEV:{Dev_Zaid}') and not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(
                   f'{cid}:rankOWNER:{id}{Dev_Zaid}') and not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
               m.reply(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}') or r.get(
                   f'{cid}:rankMOD:{id}{Dev_Zaid}'):
               return m.reply(f'{k} رتبته اعلى منك')
           else:
               return m.reply(f'{k} ماله رتبة')
