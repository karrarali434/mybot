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

@Client.on_message(filters.text & filters.group, group=12)
def getRanksHandler(c,m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f'{Dev_Zaid}:botkey')
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'eeeCASH'
    Thread(target=get_ranks_func,args=(c,m,k,channel)).start()
    
def get_ranks_func(c,m,k,channel):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_Zaid}') or r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
    
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return 
   text = m.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   if isLockCommand(m.from_user.id, m.chat.id, text): return
   if text == 'قائمه Dev':
      if not devp_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV2'):
           return m.reply(f'{k} مافيه قائمة  Dev²🎖️')
        else:
          text = '- قائمة  Dev²🎖:\n\n'
          count = 1
          for dev2 in r.smembers(f'{Dev_Zaid}DEV2'):
             if count == 101: break
             try:
               user = c.get_users(int(dev2))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(dev2)})'
               id = int(dev2)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   if text == 'قائمه MY':
      if not dev2_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV'):
          return m.reply(f'{k}  مافيه Myth🎖️ ')
        else:
          text = '- قائمة Myth🎖️:\n\n'
          count = 1
          for dev in r.smembers(f'{Dev_Zaid}DEV'):
             if count == 101: break
             try:
               user = c.get_users(int(dev))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(dev)})'
               id = int(dev)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
          
   cid = m.chat.id
   if text == 'المنشئين الاساسيين':
      if not dev_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المطور وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مالكين اساسيين ')
        else:
          text = '- المنشئين الاساسيين:\n\n'
          count = 1
          for gowner in r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(gowner))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(gowner)})'
               id = int(gowner)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
          
   if text == 'المالكين':
      if not gowner_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
      else:
        if not r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مالكيين ')
        else:
          text = '- المالكيين:\n\n'
          count = 1
          for owner in r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(owner))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(owner)})'
               id = int(owner)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   if text == 'المدراء':
      if not owner_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مدراء ')
        else:
          text = '- المدراء:\n\n'
          count = 1
          for mod in r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(mod))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(mod)})'
               id = int(mod)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   if text == 'الادمنيه':
      if not mod_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه ادمن ')
        else:
          text = '- الادمنيه:\n\n'
          count = 1
          for ADM in r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(ADM))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(ADM)})'
               id = int(ADM)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   if text == 'المشرفين':
      if not admin_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        try:
          text = '- مشرفين القروب:\n\n'
          count = 1
          for mm in c.get_chat_members(m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if count == 101: break
            if not mm.user.is_deleted and not mm.user.is_bot:
               id = mm.user.id
               username = mm.user.username
               title = mm.custom_title if hasattr(mm, 'custom_title') and mm.custom_title else 'مشرف'
               if mm.user.username:
                 text += f'{count} ➣ @{username} ࿓ {title} ࿓ ( `{id}` )\n'
               else:
                 mention = mm.user.mention
                 text += f'{count} ➣ {mention} ࿓ {title} ࿓ ( `{id}` )\n'
               count += 1
          if count == 1:
            return m.reply(f'{k} مافيه مشرفين في القروب')
          text += '\n☆'
          m.reply(text)
        except Exception as e:
          m.reply(f'{k} حدث خطأ اثناء جلب المشرفين: {e}')
   
   if text == 'المميزين':
      if not admin_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مميزين ')
        else:
          text = '- المميزين:\n\n'
          count = 1
          for PRE in r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(PRE))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(PRE)})'
               id = int(PRE)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   if text == 'المكتومين':
      if not mod_pls(m.from_user.id,m.chat.id):
        return m.reply(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مكتومين ')
        else:
          text = '- المكتومين:\n\n'
          count = 1
          for PRE in r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = c.get_users(int(PRE))
               mention = user.mention
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={PRE})'
               id = PRE
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          m.reply(text)
   
   

             
        
        
