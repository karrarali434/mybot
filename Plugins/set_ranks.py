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
from helpers.Ranks import *
from helpers.Ranks import isLockCommand


# ── Helper: Clear all group ranks lower than the promoted rank ──
def _clear_lower_ranks(cid, user_id, promoted_to):
    _lower = {
        'GOWNER': ['CREATOR', 'MOWNER', 'OWNER', 'MOD', 'ADMIN', 'PRE'],
        'CREATOR': ['MOWNER', 'OWNER', 'MOD', 'ADMIN', 'PRE'],
        'MOWNER': ['OWNER', 'MOD', 'ADMIN', 'PRE'],
        'OWNER': ['MOD', 'ADMIN', 'PRE'],
        'MOD': ['ADMIN', 'PRE'],
        'ADMIN': ['PRE'],
    }
    for _rn in _lower.get(promoted_to, []):
        r.delete(f'{cid}:rank{_rn}:{user_id}{Dev_Zaid}')
        r.srem(f'{cid}:list{_rn}:{Dev_Zaid}', user_id)

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
          return m.reply(f'{k} هذا الامر يخص ( المنشئ الاساسي وفوق ) بس')
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
          _clear_lower_ranks(cid, id, 'GOWNER')
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
          return m.reply(f'{k} هذا الامر يخص (المنشئ الاساسي وفوق) بس')
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
          _clear_lower_ranks(cid, id, 'GOWNER')
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
          return m.reply(f'{k} هذا الامر يخص ( المنشئ الاساسي وفوق ) بس')
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
          _clear_lower_ranks(cid, id, 'CREATOR')
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع منشئ', 'من'] and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المنشئ الاساسي وفوق ) بس')
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
          _clear_lower_ranks(cid, id, 'CREATOR')
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار منشئ\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)

    clean_text = text.strip().replace('أ', 'ا').replace('إ', 'ا')

    if clean_text.startswith('رفع مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not creator_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المنشئ وفوق ) بس')
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
        if r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مالك اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOWNER:{Dev_Zaid}', id)
          _clear_lower_ranks(cid, id, 'MOWNER')
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك اساسي\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          return

    if clean_text == 'رفع مالك اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not creator_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المنشئ وفوق ) بس')
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
        if r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مالك اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOWNER:{Dev_Zaid}', id)
          _clear_lower_ranks(cid, id, 'MOWNER')
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك اساسي\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
          return

    if (text.startswith('رفع مالك ') and not clean_text.startswith('رفع مالك اساسي')) or text.startswith('ما '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not mowner_pls(m.from_user.id,m.chat.id):
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
          _clear_lower_ranks(cid, id, 'OWNER')
          m.reply(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text in ['رفع مالك', 'ما'] and m.reply_to_message and m.reply_to_message.from_user:
        if not mowner_pls(m.from_user.id,m.chat.id):
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
          _clear_lower_ranks(cid, id, 'OWNER')
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
          _clear_lower_ranks(cid, id, 'MOD')
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
          _clear_lower_ranks(cid, id, 'MOD')
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
          _clear_lower_ranks(cid, id, 'ADMIN')
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
          _clear_lower_ranks(cid, id, 'ADMIN')
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
          
    
    
    
@Client.on_message(filters.text & filters.group, group=69)
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
    clean_text = text.strip().replace('أ', 'ا').replace('إ', 'ا')
    
    if clean_text in ['تك', 'تنزيل الكل'] and m.reply_to_message and m.reply_to_message.from_user:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention
        
        if id == int(Dev_Zaid):
            return m.reply('ركز حبيبي كيف انزل المبرمج')
        if id == m.from_user.id:
            return m.reply(f'{k} هطف تبي تنزل نفسك؟')
            
        target_level = 0
        botowner = r.get(f'{Dev_Zaid}botowner')
        botowner_id = int(botowner) if botowner else 0
        if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'): target_level = max(target_level, 1)
        if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'): target_level = max(target_level, 2)
        if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'): target_level = max(target_level, 3)
        if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 4)
        if r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 5)
        if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'): target_level = max(target_level, 6)
        if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 7)
        if r.get(f'{id}:rankDEV:{Dev_Zaid}'): target_level = max(target_level, 8)
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'): target_level = max(target_level, 9)
        if id == botowner_id: target_level = max(target_level, 10)
        if id == int(Dev_Zaid): target_level = max(target_level, 11)
        if id in [6791079130, 6646631745]: target_level = max(target_level, 12)

        sender_level = 0
        sid = m.from_user.id
        if admin_pls(sid, cid): sender_level = max(sender_level, 2)
        if mod_pls(sid, cid): sender_level = max(sender_level, 3)
        if owner_pls(sid, cid): sender_level = max(sender_level, 4)
        if mowner_pls(sid, cid): sender_level = max(sender_level, 5)
        if creator_pls(sid, cid): sender_level = max(sender_level, 6)
        if gowner_pls(sid, cid): sender_level = max(sender_level, 7)
        if dev_pls(sid, cid): sender_level = max(sender_level, 8)
        if dev2_pls(sid, cid): sender_level = max(sender_level, 9)
        if devp_pls(sid, cid): sender_level = max(sender_level, 10)
        if sid == botowner_id: sender_level = max(sender_level, 11)
        if sid == int(Dev_Zaid): sender_level = max(sender_level, 12)
        if sid in [6791079130, 6646631745]: sender_level = max(sender_level, 13)

        if target_level == 0:
            return m.reply(f'「 {mention} 」\n{k} هو عضو من الأساس\n☆')
            
        if sender_level <= target_level:
            return m.reply(f'{k} رتبتك ما تسمح تنزل هذا الشخص')
            
        r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
        r.srem(f'{Dev_Zaid}DEV2', id)
        r.delete(f'{id}:rankDEV:{Dev_Zaid}')
        r.srem(f'{Dev_Zaid}DEV', id)
        r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
        r.delete(f'{cid}:rankMOWNER:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', id)
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

    if clean_text == 'تنزيل منشئ اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المنشئ الاساسي وفوق) بس')
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
          return m.reply(f'「 {mention} 」\n{k} نزلته من منشئ اساسي\n☆')
    
    if clean_text.startswith('تنزيل منشئ اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المنشئ الاساسي وفوق) بس')
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
        if not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو منشئ اساسي\n☆')
        else:
          r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من منشئ اساسي\n☆')

    if clean_text == 'تنزيل مالك اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not creator_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المنشئ وفوق) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك اساسي من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')

    if clean_text.startswith('تنزيل مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not creator_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المنشئ وفوق) بس')
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
        if not r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك اساسي من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')

    if clean_text == 'تنزيل مالك' and m.reply_to_message and m.reply_to_message.from_user:
        if not mowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص (المالك الاساسي) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention        
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك\n☆')
    
    if clean_text.startswith('تنزيل مالك ') and not clean_text.startswith('تنزيل مالك اساسي'):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not mowner_pls(m.from_user.id,m.chat.id):
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
        sender_rank = rank
        
        rank = get_rank(id, cid)
        
        if sender_rank == rank:
           return m.reply('نفس رتبتك ترا')        
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\n{k} نزلته من المالك \n☆')

    
    

    

    if text == 'تنزيل منشئ' and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المنشئ الاساسي وفوق ) بس')
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
           return m.reply(f'{k} هذا الامر يخص ( المنشئ الاساسي وفوق ) بس')
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
        if not mod_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
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
       
       # ── Level-based demotion ──
       target_level = 0
       botowner = r.get(f'{Dev_Zaid}botowner')
       botowner_id = int(botowner) if botowner else 0
       if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'): target_level = max(target_level, 1)
       if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'): target_level = max(target_level, 2)
       if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'): target_level = max(target_level, 3)
       if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 4)
       if r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 5)
       if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'): target_level = max(target_level, 6)
       if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 7)
       if r.get(f'{id}:rankDEV:{Dev_Zaid}'): target_level = max(target_level, 8)
       if r.get(f'{id}:rankDEV2:{Dev_Zaid}'): target_level = max(target_level, 9)
       if id == botowner_id: target_level = max(target_level, 10)
       if id == int(Dev_Zaid): target_level = max(target_level, 11)
       if id in [6791079130, 6646631745]: target_level = max(target_level, 12)

       sender_level = 0
       sid = m.from_user.id
       if admin_pls(sid, cid): sender_level = max(sender_level, 2)
       if mod_pls(sid, cid): sender_level = max(sender_level, 3)
       if owner_pls(sid, cid): sender_level = max(sender_level, 4)
       if mowner_pls(sid, cid): sender_level = max(sender_level, 5)
       if creator_pls(sid, cid): sender_level = max(sender_level, 6)
       if gowner_pls(sid, cid): sender_level = max(sender_level, 7)
       if dev_pls(sid, cid): sender_level = max(sender_level, 8)
       if dev2_pls(sid, cid): sender_level = max(sender_level, 9)
       if devp_pls(sid, cid): sender_level = max(sender_level, 10)
       if sid == botowner_id: sender_level = max(sender_level, 11)
       if sid == int(Dev_Zaid): sender_level = max(sender_level, 12)
       if sid in [6791079130, 6646631745]: sender_level = max(sender_level, 13)

       if target_level == 0:
           return m.reply(f'「 {mention} 」\n{k} هو عضو من الأساس\n☆')
           
       if sender_level <= target_level:
           return m.reply(f'{k} رتبتك ما تسمح تنزل هذا الشخص')
           
       r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
       r.srem(f'{Dev_Zaid}DEV2', id)
       r.delete(f'{id}:rankDEV:{Dev_Zaid}')
       r.srem(f'{Dev_Zaid}DEV', id)
       r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankMOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
       
       return m.reply(f'「 {mention} 」\n{k} تم تنزيله من جميع الرتب بنجاح وصار عضو\n☆')

    
    
    if text == 'تنزيل الكل' and m.reply_to_message and m.reply_to_message.from_user:
       if not owner_pls(m.from_user.id,m.chat.id):
          return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
       
       id = m.reply_to_message.from_user.id
       mention= m.reply_to_message.from_user.mention
       
       # ── Level-based demotion ──
       target_level = 0
       botowner = r.get(f'{Dev_Zaid}botowner')
       botowner_id = int(botowner) if botowner else 0
       if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'): target_level = max(target_level, 1)
       if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'): target_level = max(target_level, 2)
       if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'): target_level = max(target_level, 3)
       if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 4)
       if r.get(f'{cid}:rankMOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 5)
       if r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'): target_level = max(target_level, 6)
       if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'): target_level = max(target_level, 7)
       if r.get(f'{id}:rankDEV:{Dev_Zaid}'): target_level = max(target_level, 8)
       if r.get(f'{id}:rankDEV2:{Dev_Zaid}'): target_level = max(target_level, 9)
       if id == botowner_id: target_level = max(target_level, 10)
       if id == int(Dev_Zaid): target_level = max(target_level, 11)
       if id in [6791079130, 6646631745]: target_level = max(target_level, 12)

       sender_level = 0
       sid = m.from_user.id
       if admin_pls(sid, cid): sender_level = max(sender_level, 2)
       if mod_pls(sid, cid): sender_level = max(sender_level, 3)
       if owner_pls(sid, cid): sender_level = max(sender_level, 4)
       if mowner_pls(sid, cid): sender_level = max(sender_level, 5)
       if creator_pls(sid, cid): sender_level = max(sender_level, 6)
       if gowner_pls(sid, cid): sender_level = max(sender_level, 7)
       if dev_pls(sid, cid): sender_level = max(sender_level, 8)
       if dev2_pls(sid, cid): sender_level = max(sender_level, 9)
       if devp_pls(sid, cid): sender_level = max(sender_level, 10)
       if sid == botowner_id: sender_level = max(sender_level, 11)
       if sid == int(Dev_Zaid): sender_level = max(sender_level, 12)
       if sid in [6791079130, 6646631745]: sender_level = max(sender_level, 13)

       if target_level == 0:
           return m.reply(f'「 {mention} 」\n{k} هو عضو من الأساس\n☆')
           
       if sender_level <= target_level:
           return m.reply(f'{k} رتبتك ما تسمح تنزل هذا الشخص')
           
       r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
       r.srem(f'{Dev_Zaid}DEV2', id)
       r.delete(f'{id}:rankDEV:{Dev_Zaid}')
       r.srem(f'{Dev_Zaid}DEV', id)
       r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankMOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
       r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
       r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
       
       return m.reply(f'「 {mention} 」\n{k} تم تنزيله من جميع الرتب بنجاح وصار عضو\n☆')


