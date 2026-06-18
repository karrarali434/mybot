import random, re, time
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand

@Client.on_message(filters.text & filters.group, group=205)
def warningsCommandsHandler(c, m):
    if not getattr(m, 'from_user', None): return
    if isLockCommand(m.from_user.id, m.chat.id, m.text): return
    k = r.get(f'{Dev_Zaid}:botkey')
    text = m.text
    name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'اتاك'
    if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
    
    cid = m.chat.id
    fid = m.from_user.id

    # تفعيل وتعطيل الانذارات
    if text == 'تعطيل الانذارات':
        if not owner_pls(fid, cid):
            return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if r.get(f'{cid}:disableWarns:{Dev_Zaid}'):
            return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} الانذارات معطلة من قبل\n☆')
        else:
            r.set(f'{cid}:disableWarns:{Dev_Zaid}', 1)
            return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر عطلت ميزة الانذارات\n☆')
            
    if text == 'تفعيل الانذارات':
        if not owner_pls(fid, cid):
            return m.reply(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if not r.get(f'{cid}:disableWarns:{Dev_Zaid}'):
            return m.reply(f'「 {m.from_user.mention} 」\n{k} الانذارات مفعلة من قبل\n☆')
        else:
            r.delete(f'{cid}:disableWarns:{Dev_Zaid}')
            return m.reply(f'{k} من「 {m.from_user.mention} 」\n{k} ابشر فعلت ميزة الانذارات\n☆')

    # التحقق إذا كانت الميزة معطلة أو البوت غير مفعل
    if not r.get(f'{cid}:enable:{Dev_Zaid}'): return
    if r.get(f'{cid}:disableWarns:{Dev_Zaid}'): return

    # أمر الانذار
    if text.startswith('انذار') or text.startswith('إنذار'):
        if not admin_pls(fid, cid):
            return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
            
        target_id = None
        mention = None
        
        # بالرد
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
            mention = m.reply_to_message.from_user.mention
        # باليوزر أو الايدي
        elif len(text.split()) >= 2:
            user = text.split()[-1]
            if user.startswith('@'):
                try:
                    get = c.get_users(user.lstrip('@'))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    return m.reply(f'{k} مافيه عضو بهذا اليوزر')
            else:
                try:
                    get = c.get_chat(int(user))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        
        if not target_id: return
        
        if target_id == fid:
            return m.reply(f'{k} هطف تبي تنذر نفسك؟')
        if target_id == int(Dev_Zaid):
            return m.reply(f'{k} ما اقدر انذر المبرمج حبيبي')
        
        # الحماية: التحقق من أن المستهدف ليس أدمن أو أعلى
        if admin_pls(target_id, cid):
            return m.reply(f'{k} ما تقدر تنذر المشرفين')
            
        # زيادة عدد الانذارات
        warns_key = f'{cid}:warns:{target_id}:{Dev_Zaid}'
        current_warns = r.get(warns_key)
        
        if not current_warns:
            current_warns = 0
        else:
            current_warns = int(current_warns)
            
        current_warns += 1
        
        if current_warns >= 3:
            # كتم العضو
            try:
                # التحقق من صلاحيات البوت أولاً
                bot_member = c.get_chat_member(cid, "me")
                if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
                    return m.reply(f'{k} البوت لا يمتلك صلاحية الكتم (تقييد الأعضاء) في هذه المجموعة.\n{k} يرجى رفع البوت كأدمن مع صلاحية الحظر/التقييد ليعمل نظام الإنذارات بشكل صحيح.')
                
                # تنفيذ الكتم
                c.restrict_chat_member(cid, target_id, ChatPermissions(can_send_messages=False))
                
                # تصفير الإنذارات بعد الكتم
                r.delete(warns_key)
                
                # تسجيل الكتم في قائمة كتم البوت الداخلي (اختياري، ليظل مكتوماً حتى لو تم فكه من التليجرام بالخطأ)
                r.set(f'{target_id}:mute:{cid}{Dev_Zaid}', 1)
                r.sadd(f'{cid}:listMUTE:{Dev_Zaid}', target_id)
                
                return m.reply(f'「 {mention} 」\n{k} هذا هو الإنذار الثالث له!\n{k} تم كتمه أوتوماتيكياً بنجاح وتصفير إنذاراته.\n☆')
            
            except Exception as e:
                r.set(warns_key, current_warns) # حفظ الانذار حتى لو فشل الكتم
                return m.reply(f'{k} حدث خطأ أثناء محاولة كتم العضو:\n`{str(e)}`')
                
        else:
            # حفظ الانذار الجديد
            r.set(warns_key, current_warns)
            return m.reply(f'「 {mention} 」\n{k} تم إعطاءه إنذار.\n{k} عدد إنذاراته الحالية: {current_warns}/3\n☆')

    # مسح الانذارات
    if text.startswith('مسح الانذارات') or text.startswith('مسح إنذارات'):
        if not admin_pls(fid, cid):
            return m.reply(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
            
        target_id = None
        mention = None
        
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
            mention = m.reply_to_message.from_user.mention
        elif len(text.split()) >= 3:
            user = text.split()[-1]
            if user.startswith('@'):
                try:
                    get = c.get_users(user.lstrip('@'))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    return m.reply(f'{k} مافيه عضو بهذا اليوزر')
            else:
                try:
                    get = c.get_chat(int(user))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    return m.reply(f'{k} مافيه عضو بهذا الآيدي')
        
        if not target_id: return
        
        warns_key = f'{cid}:warns:{target_id}:{Dev_Zaid}'
        
        if not r.get(warns_key):
            return m.reply(f'「 {mention} 」\n{k} ما عنده أي إنذارات من قبل\n☆')
        else:
            r.delete(warns_key)
            return m.reply(f'「 {mention} 」\n{k} ابشر مسحت جميع إنذاراته وتصفرت.\n☆')

    # فحص الانذارات
    if text.startswith('الانذارات') or text.startswith('إنذارات'):
        target_id = fid
        mention = f'[{m.from_user.first_name}](tg://user?id={fid})'
        
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
            mention = m.reply_to_message.from_user.mention
            
        elif len(text.split()) >= 2 and text != 'الانذارات':
            user = text.split()[-1]
            if user.startswith('@'):
                try:
                    get = c.get_users(user.lstrip('@'))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    pass
            elif re.match(r'^\d+$', user):
                try:
                    get = c.get_chat(int(user))
                    mention = f'[{get.first_name}](tg://user?id={get.id})'
                    target_id = get.id
                except:
                    pass
                    
        warns_key = f'{cid}:warns:{target_id}:{Dev_Zaid}'
        current_warns = r.get(warns_key)
        
        if not current_warns:
            current_warns = 0
            
        return m.reply(f'「 {mention} 」\n{k} عدد إنذاراته الحالية: {current_warns}/3\n☆')
