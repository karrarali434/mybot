import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/all.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "الرابط" logic
old_link_logic = '''    if text == "الرابط":
        if not r.get(f"{m.chat.id}:disableLINK:{Dev_Zaid}"):
            link = c.get_chat(m.chat.id).invite_link
            return m.reply(f"[{m.chat.title}]({link})", disable_web_page_preview=True)'''

new_link_logic = '''    if text == "الرابط":
        if not r.get(f"{m.chat.id}:disableLINK:{Dev_Zaid}"):
            if r.get(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}"):
                link = r.get(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}")
                if not link:
                    try:
                        new_link = c.create_chat_invite_link(m.chat.id, creates_join_request=True)
                        link = new_link.invite_link
                        r.set(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}", link)
                    except Exception as e:
                        return m.reply(f"{k} البوت ماعنده صلاحية دعوة المستخدمين عشان يسوي رابط طلب انضمام.")
                return m.reply(f"[{m.chat.title}]({link})", disable_web_page_preview=True)
            else:
                link = c.get_chat(m.chat.id).invite_link
                if not link:
                    try:
                        link = c.export_chat_invite_link(m.chat.id)
                    except:
                        pass
                return m.reply(f"[{m.chat.title}]({link})", disable_web_page_preview=True)'''

content = content.replace(old_link_logic, new_link_logic)

# Add command: تعطيل الرابط العادي and تفعيل الرابط العادي
new_commands = '''
    if text == "تعطيل الرابط العادي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if m.chat.username:
            return m.reply(f"{k} ما تقدر تعطل الرابط العادي بقروب عام (له يوزر)، لازم يكون خاص.")
        try:
            new_link = c.create_chat_invite_link(m.chat.id, creates_join_request=True)
            r.set(f"{m.chat.id}:JoinRequestLink:{Dev_Zaid}", new_link.invite_link)
            r.set(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}", 1)
            # Try to revoke the normal link by generating a new primary one and not giving it out
            # Or just export it so old one dies, though it's optional.
            c.export_chat_invite_link(m.chat.id)
            return m.reply(f"{k} ابشر عطلت الرابط العادي وصار يعطي رابط طلب انضمام فقط\\n☆")
        except Exception as e:
            return m.reply(f"{k} البوت ماعنده صلاحية كافية (إضافة مشرفين/إضافة مستخدمين) عشان يسوي رابط طلب.")

    if text == "تفعيل الرابط العادي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        r.delete(f"{m.chat.id}:disableNormalLink:{Dev_Zaid}")
        return m.reply(f"{k} ابشر فعلت الرابط العادي\\n☆")
'''

content = content.replace('    if text == "انشاء رابط":', new_commands + '\n    if text == "انشاء رابط":')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Link logic updated!')
