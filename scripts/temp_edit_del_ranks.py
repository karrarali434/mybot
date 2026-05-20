import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/del_ranks.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fake_rank_code = '''
   if text == 'مسح الرتب الوهميه' or text == 'مسح الرتب الوهمية':
      if not owner_pls(id, cid):
         return m.reply(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
      
      fake_count = 0
      ranks_to_check = [
           (f'{cid}:listGOWNER:{Dev_Zaid}', f'{cid}:rankGOWNER:'),
           (f'{cid}:listCREATOR:{Dev_Zaid}', f'{cid}:rankCREATOR:'),
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
                   
      return m.reply(f'{k} ابشر مسحت ( {fake_count} ) رتبة وهمية\\n☆')
'''

if 'مسح الرتب الوهميه' not in content:
    content = content.replace("   if text == 'مسح المميزين':", fake_rank_code + "\n   if text == 'مسح المميزين':")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("del_ranks.py updated")
