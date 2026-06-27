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


@Client.on_message(filters.text & filters.group, group=13)
def delRanksHandler(c,m):
    if not getattr(m, 'from_user', None): return
    k = r.get(f'{Dev_Zaid}:botkey')
    Thread(target=del_ranks_func,args=(c,m,k)).start()
    

def del_ranks_func(c,m,k):
   if not getattr(m, 'from_user', None): return
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return 
   
   if r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_Zaid}'):  return
   if r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_Zaid}'):  return 
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
   id = m.from_user.id
   cid = m.chat.id
   demoted = '''{} ابشر عيني {}
{} مسحت ( {} ) من {} 
☆
'''
   if text == 'مسح قائمه Dev':
      if not devp_pls(id, cid):
        return m.reply(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV2'):
          return m.reply(f'{k} مافيه قائمة Dev²🎖')
        else:
          count = 0
          for dev2 in r.smembers(f'{Dev_Zaid}DEV2'):
             r.srem(f'{Dev_Zaid}DEV2', int(dev2))
             r.delete(f'{int(dev2)}:rankDEV2:{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'قائمة Dev'))
   
   if text == 'مسح قائمه MY':
      if not dev2_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV'):
          return m.reply(f'{k} مافيه قائمة Myth🎖️')
        else:
          count = 0
          for dev in r.smembers(f'{Dev_Zaid}DEV'):
             r.srem(f'{Dev_Zaid}DEV', int(dev))
             r.delete(f'{int(dev)}:rankDEV:{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'قائمة MY'))
   
   if text == 'مسح المنشئين الاساسيين':
      if not dev_pls(id, cid):
        return m.reply(f'{k} هذا الامر يخص ( Myth🎖️ مالك القروب وفوق) بس')
      else:
        if not r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه منشئين اساسيين')
        else:
          count = 0
          for gowner in r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
             r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', int(gowner))
             r.delete(f'{cid}:rankGOWNER:{int(gowner)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المنشئين الاساسيين'))

   if text in ['مسح الملاكين الاساسيين', 'مسح الملاكين الأساسيين']:
      if not owner_pls(id, cid):
        return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMOWNER:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه ملاكين اساسيين')
        else:
          count = 0
          for mowner in r.smembers(f'{cid}:listMOWNER:{Dev_Zaid}'):
             r.srem(f'{cid}:listMOWNER:{Dev_Zaid}', int(mowner))
             r.delete(f'{cid}:rankMOWNER:{int(mowner)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'الملاكين الاساسيين'))
   
   if text == 'مسح المالكين':
      if not gowner_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مالكين ')
        else:
          count = 0
          for owner in r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
             r.srem(f'{cid}:listOWNER:{Dev_Zaid}', int(owner))
             r.delete(f'{cid}:rankOWNER:{int(owner)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المالكين'))
   
   if text == 'مسح المدراء':
      if not owner_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مدراء')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
             r.srem(f'{cid}:listMOD:{Dev_Zaid}', int(MOD))
             r.delete(f'{cid}:rankMOD:{int(MOD)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المدراء'))
   
   if text == 'مسح الادمنيه' or text == 'مسح الادمن':
      if not mod_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه ادمن')
        else:
          count = 0
          for ADM in r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
             r.srem(f'{cid}:listADMIN:{Dev_Zaid}', int(ADM))
             r.delete(f'{cid}:rankADMIN:{int(ADM)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'الادمن'))
   

   if text == 'مسح الرتب الوهميه' or text == 'مسح الرتب الوهمية':
      if not owner_pls(id, cid):
         return m.reply(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
      
      fake_count = 0
      ranks_to_check = [
           (f'{cid}:listGOWNER:{Dev_Zaid}', f'{cid}:rankGOWNER:'),
           (f'{cid}:listCREATOR:{Dev_Zaid}', f'{cid}:rankCREATOR:'),
           (f'{cid}:listMOWNER:{Dev_Zaid}', f'{cid}:rankMOWNER:'),
           (f'{cid}:listOWNER:{Dev_Zaid}', f'{cid}:rankOWNER:'),
           (f'{cid}:listMOD:{Dev_Zaid}', f'{cid}:rankMOD:'),
           (f'{cid}:listADMIN:{Dev_Zaid}', f'{cid}:rankADMIN:')
      ]
      
      for list_key, rank_key_prefix in ranks_to_check:
           members = r.smembers(list_key)
           for mem_id in members:
               mem_id = int(mem_id)
               if dev_pls(mem_id, cid):
                   continue
               try:
                   user_chat_member = c.get_chat_member(cid, mem_id)
                   status = user_chat_member.status
                   if status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                       r.srem(list_key, mem_id)
                       r.delete(f'{rank_key_prefix}{mem_id}{Dev_Zaid}')
                       fake_count += 1
               except Exception:
                   r.srem(list_key, mem_id)
                   r.delete(f'{rank_key_prefix}{mem_id}{Dev_Zaid}')
                   fake_count += 1
                   
      return m.reply(f'{k} ابشر مسحت ( {fake_count} ) رتبة وهمية\n☆')

   if text == 'مسح المميزين':
      if not mod_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مميزين')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
             r.srem(f'{cid}:listPRE:{Dev_Zaid}', int(MOD))
             r.delete(f'{cid}:rankPRE:{int(MOD)}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المميزين'))

   if text == 'مسح الكل' and not m.reply_to_message:
      if not owner_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
      else:
        count = 0
        ranks_lists = [
            (f'{cid}:listGOWNER:{Dev_Zaid}', f'{cid}:rankGOWNER:'),
            (f'{cid}:listCREATOR:{Dev_Zaid}', f'{cid}:rankCREATOR:'),
            (f'{cid}:listMOWNER:{Dev_Zaid}', f'{cid}:rankMOWNER:'),
            (f'{cid}:listOWNER:{Dev_Zaid}', f'{cid}:rankOWNER:'),
            (f'{cid}:listMOD:{Dev_Zaid}', f'{cid}:rankMOD:'),
            (f'{cid}:listADMIN:{Dev_Zaid}', f'{cid}:rankADMIN:'),
            (f'{cid}:listPRE:{Dev_Zaid}', f'{cid}:rankPRE:'),
        ]
        for list_key, rank_prefix in ranks_lists:
            for mem in r.smembers(list_key):
                mem_id = int(mem)
                r.srem(list_key, mem_id)
                r.delete(f'{rank_prefix}{mem_id}{Dev_Zaid}')
                count += 1
        if count == 0:
          return m.reply(f'{k} مافيه رتب بالقروب')
        return m.reply(f'{k} ابشر عيني {get_rank(id,cid)}\n{k} مسحت جميع الرتب ( {count} ) من القروب\n☆')
   
   if text == 'مسح المكتومين':
      if not mod_pls(id, cid):
        return m.reply(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مكتومين')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
             try:
               mod = int(MOD)
             except:
               mod = MOD
             r.srem(f'{cid}:listMUTE:{Dev_Zaid}', mod)
             r.delete(f'{mod}:mute:{cid}{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المكتومين'))
   
   if text == 'مسح المكتومين عام':
      if not dev_pls(id, cid):
        return m.reply(f'{k} هذا الامر يخص ( Myth🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'listMUTE:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه مكتومين عام')
        else:
          count = 0
          for MOD in r.smembers(f'listMUTE:{Dev_Zaid}'):
             r.srem(f'listMUTE:{Dev_Zaid}', int(MOD))
             r.delete(f'{int(MOD)}:mute:{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'المكتومين عام'))
   
   if text == 'مسح المحظورين عام':
      if not dev_pls(id, cid):
        return m.reply(f'{k} هذا الامر يخص ( Myth🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'listGBAN:{Dev_Zaid}'):
          return m.reply(f'{k} مافيه حمير محظورين')
        else:
          count = 0
          for MOD in r.smembers(f'listGBAN:{Dev_Zaid}'):
             r.srem(f'listGBAN:{Dev_Zaid}', int(MOD))
             r.delete(f'{int(MOD)}:gban:{Dev_Zaid}')
             count += 1
          m.reply(demoted.format(k,get_rank(id,cid),k,count,'الحمير المحظورين عام'))
          
             
       
   
   
