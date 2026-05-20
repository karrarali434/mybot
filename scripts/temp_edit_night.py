import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/all.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert night mode logic BEFORE m.media checks
night_mode_logic = '''
    if r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
        if not mod_pls(id, m.chat.id):
            if m.photo or m.voice or m.animation or m.sticker or m.video:
                try:
                    m.delete()
                except:
                    pass
                return m.reply(f"「 {mention} 」\\n{k} ممنوع إرسال الميديا بسبب الوضع الليلي\\n☆", disable_web_page_preview=True)

    if m.media:'''

content = content.replace("    if m.media:", night_mode_logic)


# 2. Insert commands for enabling and disabling
night_mode_cmds = '''
    if text == "تفعيل الوضع الليلي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
                return m.reply(f"{k} من「 {m.from_user.mention} 」\\n{k} الوضع الليلي مفعل من قبل\\n☆")
            else:
                r.set(f"{m.chat.id}:NightMode:{Dev_Zaid}", 1)
                return m.reply(f"{k} من「 {m.from_user.mention} 」\\n{k} ابشر فعلت الوضع الليلي الميديا بتنحذف\\n☆")

    if text == "تعطيل الوضع الليلي":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{m.chat.id}:NightMode:{Dev_Zaid}"):
                return m.reply(f"{k} من「 {m.from_user.mention} 」\\n{k} الوضع الليلي معطل من قبل\\n☆")
            else:
                r.delete(f"{m.chat.id}:NightMode:{Dev_Zaid}")
                return m.reply(f"{k} من「 {m.from_user.mention} 」\\n{k} ابشر عطلت الوضع الليلي\\n☆")
'''

content = content.replace('    if text == "تفعيل الحماية" or text == "تفعيل الحمايه":', night_mode_cmds + '\n    if text == "تفعيل الحماية" or text == "تفعيل الحمايه":')


# 3. Add to help menu
content = content.replace('⌯ تفعيل ↣ ↢ تعطيل الحماية\n', '⌯ تفعيل ↣ ↢ تعطيل الحماية\n⌯ تفعيل ↣ ↢ تعطيل الوضع الليلي\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Night mode implemented")
