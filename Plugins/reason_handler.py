import time
import json as _json
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from config import r, Dev_Zaid

@Client.on_message(filters.text & filters.group & filters.reply, group=5)
def reason_catcher(c, m):
    if not getattr(m, 'from_user', None) or not getattr(m, 'reply_to_message', None):
        return
        
    state_key = f"reason_req:{m.reply_to_message.id}:{m.chat.id}"
    state_data = r.get(state_key)
    
    if state_data:
        k = r.get(f'{Dev_Zaid}:botkey') or '⇜'
        try:
            data = _json.loads(state_data)
        except:
            r.delete(state_key)
            return
            
        action = data.get("action")
        target_id = data.get("target_id")
        reason = m.text
        
        # حذف حالة الانتظار لكي لا يتم الرد عليها أكثر من مرة
        r.delete(state_key)
        
        # تحديث بيانات برنت المحفوظة مسبقاً لإضافة السبب
        print_key = ""
        if action == "كتم":
            print_key = f'{m.chat.id}:print:mute:{target_id}{Dev_Zaid}'
        elif action == "كتم عام":
            print_key = f'print:gmute:{target_id}{Dev_Zaid}'
        elif action == "حظر عام":
            print_key = f'print:gban:{target_id}{Dev_Zaid}'
        elif action == "حظر عام من الالعاب":
            print_key = f'print:gbangames:{target_id}{Dev_Zaid}'
        elif action == "حظر":
            print_key = f'{m.chat.id}:print:ban:{target_id}{Dev_Zaid}'
        elif action == "طرد":
            print_key = f'{m.chat.id}:print:kick:{target_id}{Dev_Zaid}'
        elif action == "تقييد":
            print_key = f'{m.chat.id}:print:restrict:{target_id}{Dev_Zaid}'
            
        if print_key:
            old_data = r.get(print_key)
            if old_data:
                try:
                    pd = _json.loads(old_data)
                    pd["reason"] = reason
                    r.set(print_key, _json.dumps(pd))
                except:
                    pass
            else:
                # إذا لم يكن موجوداً لسبب ما
                pd = {
                    "id": m.from_user.id, 
                    "name": m.from_user.first_name, 
                    "time": int(time.time()),
                    "reason": reason
                }
                r.set(print_key, _json.dumps(pd))
                
        m.reply(f"{k} تم حفظ السبب بنجاح:\n( {reason} )")
        return
