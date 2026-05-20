code_to_append = """

@Client.on_callback_query(filters.regex(r"^prm_"))
def promote_callback(c, m):
    if not getattr(m, 'from_user', None): return
    Thread(target=promote_callback_thread, args=(c, m)).start()

def promote_callback_thread(c, m):
    k = r.get(f"{Dev_Zaid}:botkey")
    data = m.data.split("_")
    action = data[1]
    user_id = int(data[2])
    chat_id = int(data[3])
    
    if m.from_user.id != user_id:
        return m.answer("هذا الأمر لا يخصك", show_alert=True)
        
    promo_key = f"promo:{user_id}:{chat_id}"
    promo_data_str = r.get(promo_key)
    if not promo_data_str:
        return m.answer("انتهت الجلسة، الرجاء إعادة الأمر", show_alert=True)
        
    import json
    perms = json.loads(promo_data_str)
    
    if action == "cancel":
        r.delete(promo_key)
        r.delete(f"promo_target:{user_id}:{chat_id}")
        return m.edit_message_text(f"تم إلغاء رفع المشرف")
        
    if action == "all":
        for k_item in perms.keys():
            perms[k_item] = 1
        r.set(promo_key, json.dumps(perms), ex=600)
        return m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
        
    if action == "none":
        for k_item in perms.keys():
            perms[k_item] = 0
        r.set(promo_key, json.dumps(perms), ex=600)
        return m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
        
    if action == "done":
        target_id = r.get(f"promo_target:{user_id}:{chat_id}")
        if not target_id:
            return m.answer("حدث خطأ", show_alert=True)
        target_id = int(target_id)
        
        try:
            c.promote_chat_member(
                chat_id,
                target_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=bool(perms["del"]),
                    can_manage_video_chats=bool(perms["vid"]),
                    can_restrict_members=bool(perms["ban"]),
                    can_promote_members=bool(perms["promo"]),
                    can_change_info=bool(perms["info"]),
                    can_invite_users=bool(perms["inv"]),
                    can_pin_messages=bool(perms["pin"]),
                ),
            )
            get = m.message.chat.get_member(target_id)
            r.set(f"{chat_id}:rankADMIN:{get.user.id}{Dev_Zaid}", 1)
            r.sadd(f"{chat_id}:listADMIN:{Dev_Zaid}", get.user.id)
            r.delete(promo_key)
            r.delete(f"promo_target:{user_id}:{chat_id}")
            m.edit_message_text(f"الحلو 「 {get.user.mention} 」\\n{k} رفعته مشرف بالصلاحيات المحددة")
        except Exception as e:
            m.edit_message_text(f"{k} ما قدرت ارفعه، تأكد انه عضو في المجموعة")
        return
        
    # Toggle individual
    if action in perms:
        perms[action] = 1 if perms[action] == 0 else 0
        r.set(promo_key, json.dumps(perms), ex=600)
        m.edit_message_reply_markup(_build_promote_keyboard(user_id, chat_id, perms))
"""

with open('Plugins/all.py', 'a', encoding='utf-8') as f:
    f.write(code_to_append)
print("done")
