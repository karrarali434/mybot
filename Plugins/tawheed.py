'''


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/W_WT1"}
- التوحيد (Tawheed)

'''
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from config import *
from helpers.Ranks import *


@Client.on_message(filters.text & filters.group, group=88)
def tawheedHandler(c, m):
    if not getattr(m, 'from_user', None):
        return
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return
    Thread(target=tawheedFunc, args=(c, m)).start()


def tawheedFunc(c, m):
    if not getattr(m, 'from_user', None):
        return

    k = r.get(f'{Dev_Zaid}:botkey')
    text = m.text.strip()

    # ── حالة انتظار نص التوحيد من الادمن ──
    if r.get(f'{m.from_user.id}:addTawheed:{m.chat.id}:{Dev_Zaid}'):
        r.delete(f'{m.from_user.id}:addTawheed:{m.chat.id}:{Dev_Zaid}')
        # حفظ نص التوحيد في Redis
        r.set(f'{m.chat.id}:tawheed:{Dev_Zaid}', text)
        return m.reply(
            f"{k} تم حفظ التوحيد بنجاح ✅\n\n"
            f"{k} النص:\n{text}\n\n"
            f"{k} الحين أي شخص يكتب ( `التوحيد` ) بيظهر له هالنص"
        )

    # ── أمر: اضافة توحيد ──
    if text == 'اضافة توحيد' or text == 'إضافة توحيد' or text == 'اضافه توحيد' or text == 'إضافه توحيد':
        if not admin_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هالأمر للأدمن فما فوق فقط ⚠️")
        # تعيين حالة انتظار النص
        r.set(f'{m.from_user.id}:addTawheed:{m.chat.id}:{Dev_Zaid}', 1, ex=300)
        return m.reply(
            f"{k} ارسل الحين نص التوحيد الي تبي تضيفه ✍️\n\n"
            f"{k} عندك 5 دقائق لإرسال النص"
        )

    # ── أمر: مسح التوحيد ──
    if text == 'مسح التوحيد' or text == 'حذف التوحيد':
        if not admin_pls(m.from_user.id, m.chat.id):
            return m.reply(f"{k} هالأمر للأدمن فما فوق فقط ⚠️")
        if not r.get(f'{m.chat.id}:tawheed:{Dev_Zaid}'):
            return m.reply(f"{k} ما في نص توحيد محفوظ بالقروب 🚫")
        r.delete(f'{m.chat.id}:tawheed:{Dev_Zaid}')
        return m.reply(f"{k} تم مسح التوحيد بنجاح ✅")

    # ── أمر: التوحيد (عرض النص) ──
    if text == 'التوحيد':
        tawheed_text = r.get(f'{m.chat.id}:tawheed:{Dev_Zaid}')
        if not tawheed_text:
            return m.reply(f"{k} ما تم إضافة نص توحيد للقروب بعد 🚫\n{k} يقدر الأدمن يضيف بكتابة: `اضافة توحيد`")
        return m.reply(
            f"☪️ **التوحيد** ☪️\n\n"
            f"`{tawheed_text}`"
        )
