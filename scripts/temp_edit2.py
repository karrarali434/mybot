import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/set_ranks.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "من" with "ما" for OWNER
content = content.replace("startswith('من '):", "startswith('ما '):")
content = content.replace("in ['رفع مالك', 'من']", "in ['رفع مالك', 'ما']")

# Now create CREATOR logic
creator_logic = '''
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
          return m.reply(f'「 {mention} 」\\n{k} منشئ من قبل\\n☆')
        else:
          r.set(f'{cid}:rankCREATOR:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\\n{k} رفعته صار منشئ\\n☆')
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
          return m.reply(f'「 {mention} 」\\n{k} منشئ من قبل\\n☆')
        else:
          r.set(f'{cid}:rankCREATOR:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          m.reply(f'{k} الحلو 「 {mention} 」\\n{k} رفعته صار منشئ\\n☆')
          if r.get(f'{id}:mute:{m.chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{m.chat.id}{Dev_Zaid}')
            r.srem(f'{m.chat.id}:listMUTE:{Dev_Zaid}', id)
'''

# Insert creator_logic before "رفع مالك "
if 'rankCREATOR' not in content:
    content = content.replace("    if text.startswith('رفع مالك ')", creator_logic + "\n    if text.startswith('رفع مالك ')")

# Also fix the `can_demote` logic
demote_logic = '''        elif r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
            if gowner_pls(m.from_user.id, cid): can_demote = True
'''
if 'rankCREATOR' not in content:
    content = content.replace("        elif r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):", demote_logic + "        elif r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):")

# Also add to the mass `r.delete` in `تك`
delete_logic = '''        r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
        r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
'''
if 'listCREATOR' not in content.split("r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')")[0]:
    content = content.replace("        r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')", delete_logic + "        r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')")

# Now add demote logic for تنزيل منشئ
demote_creator_logic = '''
    if text == 'تنزيل منشئ' and m.reply_to_message and m.reply_to_message.from_user:
        if not gowner_pls(m.from_user.id,m.chat.id):
           return m.reply(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention        
        if id == int(Dev_Zaid):
           return m.reply('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankCREATOR:{id}{Dev_Zaid}'):
          return m.reply(f'「 {mention} 」\\n{k} مو منشئ من قبل\\n☆')
        else:
          r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\\n{k} نزلته من منشئ\\n☆')
    
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
          return m.reply(f'「 {mention} 」\\n{k} مو منشئ من قبل\\n☆')
        else:
          r.delete(f'{cid}:rankCREATOR:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listCREATOR:{Dev_Zaid}', id)
          return m.reply(f'「 {mention} 」\\n{k} نزلته من منشئ\\n☆')
'''
if 'تنزيل منشئ' not in content:
    content = content.replace("    if text == 'تنزيل مالك' and m.reply_to_message and m.reply_to_message.from_user:", demote_creator_logic + "\n    if text == 'تنزيل مالك' and m.reply_to_message and m.reply_to_message.from_user:")


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
