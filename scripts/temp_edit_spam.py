import re

file_path = 'c:/Users/LOQ/Desktop/oad/bmqa/Plugins/all.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the spam limit logic
old_spam_logic = '''    if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
        if not r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"):
            r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", 1, ex=10)
        else:
            if int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")) == 10:
                if m.from_user:
                    r.set(f"{id}:mute:{m.chat.id}{Dev_Zaid}", 1)
                    r.sadd(f"{m.chat.id}:listMUTE:{Dev_Zaid}", id)
                    r.delete(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")
                    return m.reply(
                        f"「 {mention} 」 \\n{k} كتمتك يالبثر عشان تتعلم تكرر\\n☆"
                    )

                if m.sender_chat:
                    m.chat.ban_member(m.sender_chat)
                    return m.reply(
                        f"「 {mention} 」 {k} حظرتك يالبثر عشان تتعلم تكرر\\n☆"
                    )
            else:
                get = int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"))
                r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", get + 1, ex=10)'''

new_spam_logic = '''    if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
        limit = int(r.get(f"{m.chat.id}:spamLimit:{Dev_Zaid}") or 10)
        if not r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"):
            r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", 1, ex=10)
        else:
            if int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")) >= limit:
                if m.from_user:
                    r.set(f"{id}:mute:{m.chat.id}{Dev_Zaid}", 1)
                    r.sadd(f"{m.chat.id}:listMUTE:{Dev_Zaid}", id)
                    r.delete(f"{id}in_spam:{m.chat.id}{Dev_Zaid}")
                    return m.reply(
                        f"「 {mention} 」 \\n{k} كتمتك يالبثر عشان تتعلم تكرر\\n☆"
                    )

                if m.sender_chat:
                    m.chat.ban_member(m.sender_chat.id)
                    return m.reply(
                        f"「 {mention} 」 {k} حظرتك يالبثر عشان تتعلم تكرر\\n☆"
                    )
            else:
                get = int(r.get(f"{id}in_spam:{m.chat.id}{Dev_Zaid}"))
                r.set(f"{id}in_spam:{m.chat.id}{Dev_Zaid}", get + 1, ex=10)'''

content = content.replace(old_spam_logic, new_spam_logic)

# Add the 'وضع التكرار' command
set_spam_cmd = '''
    if text.startswith("وضع التكرار "):
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        count = text.replace("وضع التكرار ", "")
        if not count.isdigit():
            return m.reply(f"{k} أرسل العدد بالأرقام فقط\\n☆")
        if int(count) < 2:
            return m.reply(f"{k} العدد لازم يكون 2 أو أكثر\\n☆")
        r.set(f"{m.chat.id}:spamLimit:{Dev_Zaid}", int(count))
        return m.reply(f"{k} ابشر تم وضع حد التكرار على {count}\\n☆")

    if text == "قفل التكرار بالكتم":
        if not mod_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}"):
                return m.reply(lockn.format(k, m.from_user.mention, k, "التكرار بالكتم"))
            else:
                r.set(f"{m.chat.id}:lockSpam:{Dev_Zaid}", 1)
                return m.reply(lock.format(k, m.from_user.mention, k, "التكرار بالكتم"))
'''

content = content.replace('    if text == "قفل التكرار":', set_spam_cmd + '\n    if text == "قفل التكرار":')

# And also add alias for 'قفل التكرار بالكتم' in the standard قفل التكرار condition?
# I already added a separate block for "قفل التكرار بالكتم" so it works identically to "قفل التكرار".
# Let's ensure text matching works well.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Spam logic updated!')
