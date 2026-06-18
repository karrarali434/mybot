import random, re, time, string
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import r, Dev_Zaid, botUsername
from helpers.Ranks import *

# ======================== مساعدات ========================

def get_team_level(points):
    """تحديد مستوى التيم بناءً على النقاط"""
    if points >= 2000:
        return "ماسي 🥇"
    elif points >= 500:
        return "فضي 🥈"
    elif points >= 100:
        return "برونزي 🥉"
    else:
        return "ضعيف"

def get_team_level_rank(points):
    """رقم مستوى التيم للمقارنة"""
    if points >= 2000: return 4
    elif points >= 500: return 3
    elif points >= 100: return 2
    else: return 1

def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def safe_str(val):
    """تحويل آمن للقيم من Redis - لأن decode_responses=True"""
    if val is None:
        return None
    if isinstance(val, bytes):
        return val.decode('utf-8')
    return str(val)

def get_daily_key():
    """مفتاح اليوم الحالي"""
    return time.strftime('%Y%m%d')

# ======================== المعالج الرئيسي ========================

@Client.on_message(filters.text & filters.group, group=125)
def teams_game_handler(c, m):
    if not getattr(m, 'from_user', None):
        return
    if r.get(f'{m.chat.id}:disableGames:{Dev_Zaid}'):
        return
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return
    if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):
        return

    k = r.get(f'{Dev_Zaid}:botkey') or '⇜'
    text = m.text
    name = r.get(f'{Dev_Zaid}:BotName') or 'اتاك'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '', 1)

    user_id = m.from_user.id
    my_team_id = r.get(f"user_team:{user_id}")

    # =====================================================
    #                    لعبة الغزاة
    # =====================================================
    if text == "الغزاة" or text == "الغزاه":
        m.reply(f"""🏴 **لعبة الغزاة (التيمات):**

أنشئ تيمك واجمع أخوياك واغزو التيمات الثانية!

🔹 `انشاء تيم [الاسم]` ← لإنشاء تيم (20,000,000 ريال)
🔹 `تيمي` أو `عتادي` ← لعرض تفاصيل تيمك
🔹 `معلومات تيمي` ← لعرض رمز الدعوة والهجوم
🔹 `اعضاء التيم` ← لعرض أعضاء التيم
🔹 `متجر الغزاه` ← لشراء العتاد الحربي
🔹 `المتجر العالمي` ← لشراء بطاقات خاصة
🔹 `دخول التيم [الرمز]` ← للانضمام لتيم
🔹 `هجوم [رمز الهجوم]` ← لغزو تيم آخر
🔹 `قصف [رمز الهجوم]` ← لقصف تيم بالصواريخ
🔹 `اظهار تيمي` ← لإظهار تيمك في التوب
🔹 `توب الغزاه` ← لعرض أقوى التيمات
""")
        return

    # =====================================================
    #                    انشاء تيم
    # =====================================================
    if text.startswith("انشاء تيم "):
        if my_team_id:
            return m.reply(f"{k} انت بالفعل في تيم! يجب ان تخرج منه أولاً.")

        team_name = text.split("انشاء تيم ", 1)[1][:30]
        if not team_name.strip():
            return m.reply(f"{k} لازم تكتب اسم التيم!")

        floos = int(r.get(f'{user_id}:Floos') or 0)
        cost = 20000000

        if floos < cost:
            return m.reply(f"{k} فلوسك ماتكفي! انشاء تيم يكلف 20,000,000 ريال وأنت معك {floos:,} ريال.")

        r.set(f'{user_id}:Floos', floos - cost)

        team_id = str(user_id) + str(int(time.time()))
        invite_code = generate_random_code(6)
        attack_code = generate_random_code(8)

        r.set(f"team:{team_id}:name", team_name)
        r.set(f"team:{team_id}:owner", user_id)
        r.set(f"team:{team_id}:invite_code", invite_code)
        r.set(f"team:{team_id}:attack_code", attack_code)
        r.set(f"team:{team_id}:points", 0)
        r.set(f"team:{team_id}:soldiers", 0)
        r.set(f"team:{team_id}:missiles", 0)
        r.set(f"team:{team_id}:anti_missiles", 0)
        r.set(f"team:{team_id}:tanks", 0)
        r.sadd(f"team:{team_id}:members", user_id)

        r.set(f"user_team:{user_id}", team_id)
        r.set(f"InviteToTeam:{invite_code}", team_id)
        r.set(f"AttackToTeam:{attack_code}", team_id)
        r.sadd("AllTeamsList", team_id)

        m.reply(f"🎉 **مبروك!** تم إنشاء تيم « {team_name} » بنجاح وتم خصم 20 مليون ريال.\nارسل `معلومات تيمي` لمعرفة رمز الدعوة ورمز الهجوم.")

    # =====================================================
    #                    مسح تيمي
    # =====================================================
    if text == "مسح تيمي":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")

        inv = r.get(f"team:{my_team_id}:invite_code")
        att = r.get(f"team:{my_team_id}:attack_code")

        # إزالة الأعضاء
        members = r.smembers(f"team:{my_team_id}:members")
        for mem in members:
            r.delete(f"user_team:{mem}")

        # إزالة رموز الدعوة والهجوم
        if inv:
            r.delete(f"InviteToTeam:{inv}")
        if att:
            r.delete(f"AttackToTeam:{att}")
        r.srem("AllTeamsList", my_team_id)

        # إزالة قائمة الحظر
        for key in r.keys(f"team:{my_team_id}:banned:*"):
            r.delete(key)

        # حذف جميع مفاتيح التيم
        for key in r.keys(f"team:{my_team_id}:*"):
            r.delete(key)

        m.reply(f"🗑 تم مسح التيم بالكامل وطرد جميع الأعضاء وتصفير العتاد.")

    # =====================================================
    #                    معلومات تيمي
    # =====================================================
    if text == "معلومات تيمي":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")

        inv = r.get(f"team:{my_team_id}:invite_code")
        att = r.get(f"team:{my_team_id}:attack_code")
        t_name = r.get(f"team:{my_team_id}:name") or "بدون اسم"
        try:
            c.send_message(user_id, f"""🏰 **معلومات تيمك السرية:**
🏴 **اسم التيم:** {t_name}

📌 **رمز الدعوة** (لإدخال أخوياك): `{inv}`
💣 **رمز الهجوم** (تستقبل منه الهجمات): `{att}`

⚠️ **تحذير:** لا تشارك رمز الهجوم مع أحد إلا للعدو، ولا تشارك رمز الدعوة إلا لأصدقائك.""")
            m.reply(f"{k} تم إرسال الرموز في الخاص حفاظاً على السرية 🔒")
        except:
            m.reply(f"{k} افتح الخاص أولاً عشان أرسل لك الرموز!")

    # =====================================================
    #                عتادي / تيمي
    # =====================================================
    if text in ["عتادي", "تيمي"]:
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")

        t_name = r.get(f"team:{my_team_id}:name") or "بدون اسم"
        pts = int(r.get(f"team:{my_team_id}:points") or 0)
        lvl = get_team_level(pts)
        m_count = r.scard(f"team:{my_team_id}:members")

        sol = int(r.get(f"team:{my_team_id}:soldiers") or 0)
        mis = int(r.get(f"team:{my_team_id}:missiles") or 0)
        amis = int(r.get(f"team:{my_team_id}:anti_missiles") or 0)
        tan = int(r.get(f"team:{my_team_id}:tanks") or 0)

        vis = "ظاهر 👁" if r.get(f"team:{my_team_id}:visible") else "مخفي 👻"
        lock_att = "مقفل 🔒" if r.get(f"team:{my_team_id}:attack_locked") else "مفتوح 🔓"
        lock_join = "مقفل 🔒" if r.get(f"team:{my_team_id}:locked") else "مفتوح 🔓"

        # حساب القوة الإجمالية
        total_power = sol + (tan * 10)

        m.reply(f"""🏴 **تيم:** {t_name}

🔰 **المستوى:** {lvl}
💎 **النقاط:** {pts:,}
👥 **الأعضاء:** {m_count}/20
👁 **حالة الظهور:** {vis}
🔒 **الهجوم:** {lock_att}
🚪 **الدخول:** {lock_join}

⚔️ **العتاد الحربي:**
🪖 جنود: {sol:,}
🚀 صواريخ: {mis:,}
🛡 مضادات صواريخ: {amis:,}
🚜 دبابات: {tan:,}
💪 **القوة الإجمالية:** {total_power:,}

ارسل `اعضاء التيم` لرؤية الأعضاء.
ارسل `متجر الغزاه` لشراء العتاد.
""")

    # =====================================================
    #                 قفل الهجوم / فتح الهجوم
    # =====================================================
    if text == "قفل الهجوم":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")

        if r.get(f"team:{my_team_id}:attack_locked"):
            return m.reply(f"{k} الهجوم مقفل بالفعل على تيمك!")

        r.set(f"team:{my_team_id}:attack_locked", 1, ex=21600)  # 6 ساعات
        m.reply(f"""🔒 **تم قفل الهجوم والقصف على تيمك لمدة 6 ساعات!**

⚠️ خلال فترة القفل:
- لا يمكن لأي تيم الهجوم عليكم أو قصفكم.
- لا يمكنكم أنتم أيضاً الهجوم أو القصف على غيركم.
""")

    if text == "فتح الهجوم":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")

        if not r.get(f"team:{my_team_id}:attack_locked"):
            return m.reply(f"{k} الهجوم مفتوح بالفعل!")

        r.delete(f"team:{my_team_id}:attack_locked")
        m.reply(f"🔓 تم فتح الهجوم! الآن يمكنكم الهجوم والقصف ويمكن للآخرين مهاجمتكم.")

    # =====================================================
    #          حظر / طرد بالرد واليوزر
    # =====================================================
    if text.startswith("طرد ") or text.startswith("حظر "):
        if not my_team_id:
            return
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} المالك فقط يقدر يطرد أو يحظر.")

        is_ban = text.startswith("حظر ")

        target_id = None
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
        else:
            try:
                parts = text.split()
                if len(parts) >= 2:
                    # يمكن أن يكون آيدي رقمي أو يوزرنيم
                    try:
                        target_id = int(parts[1])
                    except:
                        # محاولة جلب بواسطة اليوزرنيم
                        try:
                            user_obj = c.get_users(parts[1])
                            target_id = user_obj.id
                        except:
                            pass
            except:
                pass

        if not target_id:
            return m.reply(f"{k} بالرد على العضو أو حط الآيدي/اليوزر حقه.")
        if target_id == user_id:
            return m.reply(f"{k} ما تقدر تطرد/تحظر نفسك!")

        if not r.sismember(f"team:{my_team_id}:members", target_id):
            if is_ban:
                # حظر شخص حتى لو مو بالتيم (يمنعه من الدخول مستقبلاً)
                r.set(f"team:{my_team_id}:banned:{target_id}", 1)
                return m.reply(f"🚫 تم حظر الشخص من دخول التيم مستقبلاً.")
            return m.reply(f"{k} هذا الشخص مو بتيمك أصلاً.")

        r.srem(f"team:{my_team_id}:members", target_id)
        r.delete(f"user_team:{target_id}")

        if is_ban:
            r.set(f"team:{my_team_id}:banned:{target_id}", 1)
            m.reply(f"🚫👢 تم طرد وحظر العضو من التيم! لن يستطيع الدخول مرة أخرى.")
        else:
            m.reply(f"👢 تم طرد العضو من التيم بنجاح.")

    # =====================================================
    #               قفل / فتح دخول التيم
    # =====================================================
    if text == "قفل دخول التيم":
        if not my_team_id:
            return
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner == user_id:
            r.set(f"team:{my_team_id}:locked", 1)
            m.reply(f"🔒 تم قفل دخول التيم. لن يستطيع أحد الانضمام حتى لو معاه رمز الدعوة.")

    if text == "فتح دخول التيم":
        if not my_team_id:
            return
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner == user_id:
            r.delete(f"team:{my_team_id}:locked")
            m.reply(f"🔓 تم فتح دخول التيم. يقدرون الناس ينضمون برمز الدعوة.")

    # =====================================================
    #                  دخول التيم
    # =====================================================
    if text.startswith("دخول التيم "):
        parts = text.split()
        if len(parts) < 3:
            return m.reply(f"{k} ارسل: `دخول التيم [رمز الدعوة]`")
        code = parts[2]
        target_team = r.get(f"InviteToTeam:{code}")

        if my_team_id:
            return m.reply(f"❌ انت مسجل بتيم بالفعل. ارسل `خروج من التيم` أولاً.")
        if not target_team:
            return m.reply(f"❌ رمز الدعوة غير صحيح.")

        target_team = safe_str(target_team)

        if r.get(f"team:{target_team}:locked"):
            return m.reply(f"❌ الدخول لهذا التيم مقفل حالياً.")

        # التحقق من الحظر
        if r.get(f"team:{target_team}:banned:{user_id}"):
            return m.reply(f"🚫 أنت محظور من هذا التيم ولا يمكنك الدخول!")

        m_count = r.scard(f"team:{target_team}:members")
        if m_count >= 20:
            return m.reply(f"❌ التيم ممتلئ (20/20)!")

        r.sadd(f"team:{target_team}:members", user_id)
        r.set(f"user_team:{user_id}", target_team)
        t_name = r.get(f"team:{target_team}:name") or "بدون اسم"
        m.reply(f"✅ تم الانضمام بنجاح إلى تيم « {t_name} »!")

    # =====================================================
    #                 خروج من التيم
    # =====================================================
    if text == "خروج من التيم":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم.")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner == user_id:
            return m.reply(f"❌ أنت مالك التيم! لا يمكنك الخروج، يجب عليك استخدام أمر `مسح تيمي`.")

        r.srem(f"team:{my_team_id}:members", user_id)
        r.delete(f"user_team:{user_id}")
        m.reply(f"🚶‍♂️ لقد خرجت من التيم بنجاح.")

    # =====================================================
    #                  اعضاء التيم
    # =====================================================
    if text == "اعضاء التيم":
        if not my_team_id:
            return m.reply(f"{k} انت مو بتيم.")

        members = r.smembers(f"team:{my_team_id}:members")
        t_name = r.get(f"team:{my_team_id}:name") or "بدون اسم"
        owner_id_team = int(r.get(f"team:{my_team_id}:owner") or 0)
        txt = f"👥 **أعضاء تيم « {t_name} »:**\n\n"

        best_buyer = None
        max_buy = -1
        best_attacker = None
        max_attack = -1

        for mem in members:
            mid = int(mem)
            try:
                u_info = c.get_users(mid)
                u_name = u_info.first_name[:15]
            except:
                u_name = str(mid)

            bought = int(r.get(f"team:{my_team_id}:member_stats:{mid}:bought") or 0)
            attacks = int(r.get(f"team:{my_team_id}:member_stats:{mid}:attacks") or 0)

            if bought > max_buy:
                max_buy = bought
                best_buyer = u_name
            if attacks > max_attack:
                max_attack = attacks
                best_attacker = u_name

            role = "👑" if mid == owner_id_team else "👤"
            txt += f"{role} {u_name}"
            if bought > 0 or attacks > 0:
                txt += f" (🛒{bought} | ⚔️{attacks})"
            txt += "\n"

        txt += f"\n💰 **أكثر مشتري للعتاد:** {best_buyer or 'لا يوجد'} ({max_buy if max_buy > 0 else 0})\n"
        txt += f"⚔️ **أكثر مهاجم للتيم:** {best_attacker or 'لا يوجد'} ({max_attack if max_attack > 0 else 0})\n"
        m.reply(txt)

    # =====================================================
    #               اظهار / اخفاء تيمي
    # =====================================================
    if text == "اظهار تيمي":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")
        r.set(f"team:{my_team_id}:visible", 1)
        m.reply(f"""👁 **تم إظهار التيم في التوب!**

✅ الآن يمكنكم الهجوم على التيمات الأخرى.
⚠️ لكن تذكر، التيمات الأخرى أيضاً تقدر تهجم عليكم.
""")

    if text == "اخفاء تيمي":
        if not my_team_id:
            return m.reply(f"{k} انت لست في تيم!")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")
        r.delete(f"team:{my_team_id}:visible")
        m.reply(f"👻 تم إخفاء التيم من التوب. لن تستطيعوا الهجوم على أحد ولن يهجم عليكم أحد.")

    # =====================================================
    #                 متجر الغزاة
    # =====================================================
    if text == "متجر الغزاه" or text == "متجر الغزاة":
        m.reply(f"""🛒 **متجر الغزاة (للتيمات):**

يتم الشراء من رصيدك الشخصي (ريال) والعتاد يذهب لتيمك!

🪖 **جنود** (1 جندي = 5,000 ريال)
`شراء جنود [العدد]`

🚀 **صواريخ** (1 صاروخ = 50,000 ريال)
`شراء صواريخ [العدد]`

🛡 **مضاد صواريخ** (1 مضاد = 100,000 ريال)
`شراء مضادات [العدد]`

🚜 **دبابات** (1 دبابة = 200,000 ريال)
`شراء دبابات [العدد]`

━━━━━━━━━
💡 كل ماتشتري أكثر يصير تيمك أقوى بالغزوات!
""")

    # =====================================================
    #                  الشراء للتيم
    # =====================================================
    if text.startswith("شراء ") and len(text.split()) == 3:
        item_type = text.split()[1]
        # تأكد إنه من عتاد التيم وليس من موارد القلاع أو بطاقات
        if item_type not in ["جنود", "صواريخ", "مضادات", "دبابات"]:
            return  # اتركه للأوامر الأخرى

        if not my_team_id:
            return m.reply(f"{k} لازم تدخل تيم أول!")

        try:
            amount = int(text.split()[2])
        except:
            return m.reply(f"{k} العدد غير صحيح.")

        if amount <= 0:
            return m.reply(f"{k} العدد لازم يكون أكبر من صفر.")
        if amount > 100000:
            return m.reply(f"{k} الحد الأقصى للشراء 100,000 بالمرة الواحدة.")

        cost = 0
        key = ""
        if item_type == "جنود":
            cost = amount * 5000
            key = "soldiers"
        elif item_type == "صواريخ":
            cost = amount * 50000
            key = "missiles"
        elif item_type == "مضادات":
            cost = amount * 100000
            key = "anti_missiles"
        elif item_type == "دبابات":
            cost = amount * 200000
            key = "tanks"

        floos = int(r.get(f'{user_id}:Floos') or 0)
        if floos < cost:
            return m.reply(f"❌ فلوسك ماتكفي! تحتاج {cost:,} ريال وأنت معك {floos:,} ريال.")

        r.set(f'{user_id}:Floos', floos - cost)
        curr = int(r.get(f"team:{my_team_id}:{key}") or 0)
        r.set(f"team:{my_team_id}:{key}", curr + amount)

        # تحديث إحصائيات العضو
        m_bought = int(r.get(f"team:{my_team_id}:member_stats:{user_id}:bought") or 0)
        r.set(f"team:{my_team_id}:member_stats:{user_id}:bought", m_bought + amount)

        m.reply(f"✅ تم شراء **{amount:,}** من {item_type} لتيمك بنجاح!\n💸 تم خصم **{cost:,}** ريال من رصيدك.")

    # =====================================================
    #                 المتجر العالمي
    # =====================================================
    if text == "المتجر العالمي":
        # التحقق من إعادة التعبئة كل 10 ساعات
        if not r.get("GlobalStore:reset_time"):
            r.set("GlobalStore:reset_time", 1, ex=36000)  # 10 ساعات
            r.set("GlobalStore:skip_time_cards", 10)
            r.set("GlobalStore:name_change_cards", 5)
            r.set("GlobalStore:invite_change_cards", 5)

        ttl_val = r.ttl("GlobalStore:reset_time")
        if ttl_val and ttl_val > 0:
            wait = time.strftime('%H:%M:%S', time.gmtime(ttl_val))
        else:
            wait = "00:00:00"

        c1 = int(r.get("GlobalStore:skip_time_cards") or 0)
        c2 = int(r.get("GlobalStore:name_change_cards") or 0)
        c3 = int(r.get("GlobalStore:invite_change_cards") or 0)

        m.reply(f"""🌍 **المتجر العالمي المحدود:**
⏳ يتصفر المتجر بعد: **{wait}**

━━━━━━━━━

💳 **بطاقة تجاوز الوقت** (تجاوز وقت انتظار الهجوم)
📦 الكمية المتبقية: **{c1}** | 💰 السعر: **10,000,000** ريال
للشراء: `شراء بطاقة تجاوز`

💳 **بطاقة تغيير اسم التيم**
📦 الكمية المتبقية: **{c2}** | 💰 السعر: **20,000,000** ريال
للشراء: `شراء بطاقة اسم`

💳 **بطاقة تغيير رمز الدعوة**
📦 الكمية المتبقية: **{c3}** | 💰 السعر: **15,000,000** ريال
للشراء: `شراء بطاقة رمز`

━━━━━━━━━
⚠️ الكمية محدودة لجميع التيمات! ما تلحق عليها تروح.
""")

    # =====================================================
    #                 شراء بطاقات
    # =====================================================
    if text.startswith("شراء بطاقة "):
        if not my_team_id:
            return m.reply(f"{k} لازم تكون بتيم عشان تشتري بطاقات.")

        ctype = text.split("بطاقة ")[1].strip()
        cost = 0
        s_key = ""
        p_key = ""
        card_name = ""

        if ctype == "تجاوز":
            cost = 10000000
            s_key = "skip_time_cards"
            p_key = "skip_time"
            card_name = "بطاقة تجاوز الوقت"
        elif ctype == "اسم":
            cost = 20000000
            s_key = "name_change_cards"
            p_key = "name_change"
            card_name = "بطاقة تغيير الاسم"
        elif ctype == "رمز":
            cost = 15000000
            s_key = "invite_change_cards"
            p_key = "invite_change"
            card_name = "بطاقة تغيير الرمز"
        else:
            return

        avail = int(r.get(f"GlobalStore:{s_key}") or 0)
        if avail <= 0:
            return m.reply(f"❌ نفذت الكمية من المتجر! انتظر التجديد.")

        floos = int(r.get(f'{user_id}:Floos') or 0)
        if floos < cost:
            return m.reply(f"❌ فلوسك ماتكفي! السعر {cost:,} ريال وأنت معك {floos:,} ريال.")

        r.set(f'{user_id}:Floos', floos - cost)
        r.set(f"GlobalStore:{s_key}", avail - 1)

        my_cards = int(r.get(f"user_cards:{user_id}:{p_key}") or 0)
        r.set(f"user_cards:{user_id}:{p_key}", my_cards + 1)
        m.reply(f"✅ تم شراء **{card_name}** بنجاح!\n💳 أصبح لديك الآن {my_cards + 1} بطاقة.\nلمعرفة طريقة الاستخدام اكتب `استخدام البطائق`")

    # =====================================================
    #                 استخدام البطائق
    # =====================================================
    if text == "استخدام البطائق":
        c1 = int(r.get(f"user_cards:{user_id}:skip_time") or 0)
        c2 = int(r.get(f"user_cards:{user_id}:name_change") or 0)
        c3 = int(r.get(f"user_cards:{user_id}:invite_change") or 0)
        m.reply(f"""💳 **بطاقاتك المتاحة:**

⏩ بطاقة تجاوز الوقت: **{c1}**
↳ للاستخدام: `استخدام بطاقة تجاوز`

✏️ بطاقة تغيير الاسم: **{c2}**
↳ للاستخدام: `استخدام بطاقة اسم [الاسم الجديد]`

🔄 بطاقة تغيير الرمز: **{c3}**
↳ للاستخدام: `استخدام بطاقة رمز`
""")

    if text.startswith("استخدام بطاقة "):
        if not my_team_id:
            return m.reply(f"{k} لازم تكون بتيم!")

        owner = int(r.get(f"team:{my_team_id}:owner") or 0)

        parts = text.split()
        if len(parts) < 3:
            return

        ctype = parts[2]

        if ctype == "تجاوز":
            c_have = int(r.get(f"user_cards:{user_id}:skip_time") or 0)
            if c_have <= 0:
                return m.reply(f"❌ ماتملك بطاقة تجاوز الوقت!")
            r.set(f"user_cards:{user_id}:skip_time", c_have - 1)
            r.delete(f"team:{my_team_id}:attack_cooldown")
            m.reply(f"✅ تم تجاوز وقت انتظار الهجوم لتيمك! يمديكم تهجمون الآن.")

        elif ctype == "اسم":
            if owner != user_id:
                return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")
            c_have = int(r.get(f"user_cards:{user_id}:name_change") or 0)
            if c_have <= 0:
                return m.reply(f"❌ ماتملك بطاقة تغيير الاسم!")
            new_name = text.replace("استخدام بطاقة اسم ", "", 1).strip()
            if not new_name:
                return m.reply(f"{k} لازم تكتب الاسم الجديد!")
            r.set(f"user_cards:{user_id}:name_change", c_have - 1)
            r.set(f"team:{my_team_id}:name", new_name[:30])
            m.reply(f"✅ تم تغيير اسم التيم إلى « {new_name[:30]} »")

        elif ctype == "رمز":
            if owner != user_id:
                return m.reply(f"{k} هذا الأمر لمالك التيم فقط.")
            c_have = int(r.get(f"user_cards:{user_id}:invite_change") or 0)
            if c_have <= 0:
                return m.reply(f"❌ ماتملك بطاقة تغيير الرمز!")
            r.set(f"user_cards:{user_id}:invite_change", c_have - 1)
            old_inv = r.get(f"team:{my_team_id}:invite_code")
            if old_inv:
                r.delete(f"InviteToTeam:{old_inv}")
            new_inv = generate_random_code(6)
            r.set(f"team:{my_team_id}:invite_code", new_inv)
            r.set(f"InviteToTeam:{new_inv}", my_team_id)
            m.reply(f"✅ تم تغيير رمز الدعوة بنجاح! ارسل `معلومات تيمي` لتشوف الرمز الجديد.")

    # =====================================================
    #              الهجوم (الغزو)
    # =====================================================
    if text.startswith("هجوم ") and len(text.split()) == 2:
        if not my_team_id:
            return m.reply(f"{k} لازم تكون بتيم عشان تهجم.")
        if not r.get(f"team:{my_team_id}:visible"):
            return m.reply(f"❌ تيمك مخفي! لازم تفعل `اظهار تيمي` عشان تقدر تهجم.")

        # التحقق من قفل الهجوم على تيمك
        if r.get(f"team:{my_team_id}:attack_locked"):
            return m.reply(f"🔒 الهجوم مقفل على تيمك حالياً! لا يمكنك الهجوم. ارسل `فتح الهجوم` أولاً.")

        target_code = text.split()[1]
        target_team = r.get(f"AttackToTeam:{target_code}")
        if not target_team:
            return m.reply(f"❌ رمز هجوم الخصم غير صحيح.")
        target_team = safe_str(target_team)

        if target_team == my_team_id:
            return m.reply(f"{k} تبي تهجم على تيمك؟ 😂")
        if not r.get(f"team:{target_team}:visible"):
            return m.reply(f"❌ هذا التيم مخفي حالياً ولا يمكن الهجوم عليه.")

        # التحقق من قفل الهجوم على تيم الخصم
        if r.get(f"team:{target_team}:attack_locked"):
            return m.reply(f"🔒 هذا التيم مفعل قفل الهجوم! لا يمكنك الهجوم عليه حالياً.")

        # التحقق من مستوى التيمات
        my_pts = int(r.get(f"team:{my_team_id}:points") or 0)
        tar_pts = int(r.get(f"team:{target_team}:points") or 0)

        if get_team_level_rank(my_pts) != get_team_level_rank(tar_pts):
            return m.reply(f"❌ مستوى التيمات مختلف!\nأنت في مستوى **{get_team_level(my_pts)}** والخصم في مستوى **{get_team_level(tar_pts)}**.\nما تقدر تهجم إلا على تيم بنفس مستواك.")

        # التحقق من وقت الانتظار
        if r.get(f"team:{my_team_id}:attack_cooldown"):
            ttl_val = r.ttl(f"team:{my_team_id}:attack_cooldown")
            if ttl_val and ttl_val > 0:
                wait = time.strftime('%M:%S', time.gmtime(ttl_val))
                return m.reply(f"⏳ تيمك مجهد من الحرب! انتظر **{wait}** دقيقة.\n💡 أو استخدم `استخدام بطاقة تجاوز` لتجاوز الوقت.")
            else:
                r.delete(f"team:{my_team_id}:attack_cooldown")

        # تعيين وقت الانتظار (30 دقيقة)
        r.set(f"team:{my_team_id}:attack_cooldown", 1, ex=1800)

        # حساب القتال
        my_sol = int(r.get(f"team:{my_team_id}:soldiers") or 0)
        my_tan = int(r.get(f"team:{my_team_id}:tanks") or 0)
        my_power = my_sol + (my_tan * 10)

        tar_sol = int(r.get(f"team:{target_team}:soldiers") or 0)
        tar_tan = int(r.get(f"team:{target_team}:tanks") or 0)
        tar_power = tar_sol + (tar_tan * 10)

        tar_name = r.get(f"team:{target_team}:name") or "الخصم"
        my_name = r.get(f"team:{my_team_id}:name") or "تيمك"

        # إضافة عنصر عشوائي للمعركة (±20%)
        luck_factor = random.uniform(0.8, 1.2)
        my_effective = int(my_power * luck_factor)

        if my_effective > tar_power:
            # فوز
            loot_pts = max(10, tar_pts // 10)
            soldiers_killed = min(tar_sol, my_sol // 5)
            tanks_destroyed = min(tar_tan, my_tan // 10)

            r.set(f"team:{target_team}:points", max(0, tar_pts - loot_pts))
            r.set(f"team:{my_team_id}:points", my_pts + loot_pts)
            r.set(f"team:{target_team}:soldiers", max(0, tar_sol - soldiers_killed))
            r.set(f"team:{target_team}:tanks", max(0, tar_tan - tanks_destroyed))

            # خسائر المهاجم (10%)
            my_losses = my_sol // 10
            r.set(f"team:{my_team_id}:soldiers", max(0, my_sol - my_losses))

            # تحديث إحصائيات العضو
            m_att = int(r.get(f"team:{my_team_id}:member_stats:{user_id}:attacks") or 0)
            r.set(f"team:{my_team_id}:member_stats:{user_id}:attacks", m_att + 1)

            # تسجيل فوز الهجوم للمهام اليومية
            daily_key = f"team:{my_team_id}:daily_wins:{get_daily_key()}"
            daily_wins = int(r.get(daily_key) or 0)
            r.set(daily_key, daily_wins + 1, ex=86400)

            m.reply(f"""⚔️ **غزوة ناجحة!** 🎉

🏴 تيم **{my_name}** ⚔️ تيم **{tar_name}**

✅ **النتيجة: انتصار!**
💎 كسبتم **{loot_pts}** نقطة
🪖 قتلتم **{soldiers_killed:,}** جندي من الخصم
🚜 دمرتم **{tanks_destroyed:,}** دبابة من الخصم
💀 خسائركم: **{my_losses:,}** جندي

💪 قوتكم: {my_power:,} | قوة الخصم: {tar_power:,}
""")
        else:
            # خسارة
            loss_pts = max(5, my_pts // 15)
            my_soldiers_lost = min(my_sol, tar_sol // 5)
            my_tanks_lost = min(my_tan, tar_tan // 10)

            r.set(f"team:{my_team_id}:points", max(0, my_pts - loss_pts))
            r.set(f"team:{my_team_id}:soldiers", max(0, my_sol - my_soldiers_lost))
            r.set(f"team:{my_team_id}:tanks", max(0, my_tan - my_tanks_lost))

            m.reply(f"""💀 **هزيمة نكراء!**

🏴 تيم **{my_name}** ⚔️ تيم **{tar_name}**

❌ **النتيجة: هزيمة!**
💔 خسرتم **{loss_pts}** نقطة
🪖 فقدتم **{my_soldiers_lost:,}** جندي
🚜 دُمرت **{my_tanks_lost:,}** دبابة

💪 قوتكم: {my_power:,} | قوة الخصم: {tar_power:,}
""")

    # =====================================================
    #                    القصف
    # =====================================================
    if text.startswith("قصف ") and len(text.split()) == 2:
        if not my_team_id:
            return m.reply(f"{k} لازم تكون بتيم عشان تقصف.")
        if not r.get(f"team:{my_team_id}:visible"):
            return m.reply(f"❌ تيمك مخفي! لازم تفعل `اظهار تيمي`.")

        # التحقق من قفل الهجوم
        if r.get(f"team:{my_team_id}:attack_locked"):
            return m.reply(f"🔒 الهجوم مقفل على تيمك حالياً!")

        target_code = text.split()[1]
        target_team = r.get(f"AttackToTeam:{target_code}")
        if not target_team:
            return m.reply(f"❌ رمز هجوم الخصم غير صحيح.")
        target_team = safe_str(target_team)

        if target_team == my_team_id:
            return m.reply(f"{k} ما تقدر تقصف نفسك!")
        if not r.get(f"team:{target_team}:visible"):
            return m.reply(f"❌ هذا التيم مخفي حالياً.")

        # التحقق من قفل الهجوم على الخصم
        if r.get(f"team:{target_team}:attack_locked"):
            return m.reply(f"🔒 هذا التيم مفعل قفل الهجوم!")

        # التحقق من المستوى
        my_pts = int(r.get(f"team:{my_team_id}:points") or 0)
        tar_pts = int(r.get(f"team:{target_team}:points") or 0)
        if get_team_level_rank(my_pts) != get_team_level_rank(tar_pts):
            return m.reply(f"❌ مستوى التيمات مختلف! أنت **{get_team_level(my_pts)}** والخصم **{get_team_level(tar_pts)}**.")

        # التحقق من الصواريخ
        my_mis = int(r.get(f"team:{my_team_id}:missiles") or 0)
        if my_mis <= 0:
            return m.reply(f"🚀 تيمك ماعنده أي صواريخ للقصف! اشترِ من `متجر الغزاه`.")

        tar_name = r.get(f"team:{target_team}:name") or "الخصم"
        my_name = r.get(f"team:{my_team_id}:name") or "تيمك"

        # إطلاق صاروخ واحد
        r.set(f"team:{my_team_id}:missiles", my_mis - 1)
        tar_amis = int(r.get(f"team:{target_team}:anti_missiles") or 0)

        if tar_amis > 0:
            # تم التصدي
            r.set(f"team:{target_team}:anti_missiles", tar_amis - 1)
            m.reply(f"""🛡 **تم التصدي للقصف!**

🚀 تيم **{my_name}** قصف تيم **{tar_name}**

🛡 تيم الخصم يمتلك **مضاد صواريخ** وتم تفجير صاروخكم في الجو!
📦 الخصم استهلك 1 مضاد صواريخ (متبقي: {tar_amis - 1})
🚀 صواريخكم المتبقية: {my_mis - 1}
""")
        else:
            # إصابة مباشرة
            dmg_pts = 50
            r.set(f"team:{target_team}:points", max(0, tar_pts - dmg_pts))
            r.set(f"team:{my_team_id}:points", my_pts + 10)

            tar_sol = int(r.get(f"team:{target_team}:soldiers") or 0)
            soldiers_killed = min(tar_sol, 1000)
            r.set(f"team:{target_team}:soldiers", max(0, tar_sol - soldiers_killed))

            tar_tan = int(r.get(f"team:{target_team}:tanks") or 0)
            tanks_destroyed = min(tar_tan, random.randint(1, 5))
            r.set(f"team:{target_team}:tanks", max(0, tar_tan - tanks_destroyed))

            # تسجيل للمهام اليومية
            daily_key = f"team:{my_team_id}:daily_wins:{get_daily_key()}"
            daily_wins = int(r.get(daily_key) or 0)
            r.set(daily_key, daily_wins + 1, ex=86400)

            m.reply(f"""💥 **بـــوووووم!** 💣

🚀 تيم **{my_name}** قصف تيم **{tar_name}**

🎯 **إصابة مباشرة!**
💎 الخصم خسر **{dmg_pts}** نقطة | كسبتم **10** نقاط
🪖 قتلتم **{soldiers_killed:,}** جندي من الخصم
🚜 دمرتم **{tanks_destroyed}** دبابة
🚀 صواريخكم المتبقية: **{my_mis - 1}**
""")

    # =====================================================
    #               مهام التيم
    # =====================================================
    if text in ["المهام", "مهام التيم"]:
        if not my_team_id:
            return m.reply(f"{k} انت مو بتيم.")

        curr_date = get_daily_key()

        # التحقق من إكمال المهام
        if r.get(f"team:{my_team_id}:task_claimed:{curr_date}"):
            return m.reply(f"✅ تيمكم خلص المهام اليومية واستلم الجائزة! تعالوا بكرة.")

        daily_wins = int(r.get(f"team:{my_team_id}:daily_wins:{curr_date}") or 0)
        target_wins = 3

        t_name = r.get(f"team:{my_team_id}:name") or "تيمك"

        progress_bar = ""
        for i in range(target_wins):
            if i < daily_wins:
                progress_bar += "🟢"
            else:
                progress_bar += "⚫"

        status = "✅ مكتملة!" if daily_wins >= target_wins else f"🔄 جاري ({daily_wins}/{target_wins})"

        m.reply(f"""📋 **مهام تيم « {t_name} » اليومية:**

━━━━━━━━━

**المهمة: الفوز بـ {target_wins} غزوات أو قصف ناجح**
{progress_bar} | {status}

━━━━━━━━━

🎁 **الجائزة:** عشوائية (فلوس / نقاط تيم / بطاقة نادرة / عتاد)
👑 يستلمها مالك التيم بأمر `جائزة المهام`
""")

    # =====================================================
    #                جائزة المهام
    # =====================================================
    if text == "جائزة المهام":
        if not my_team_id:
            return m.reply(f"{k} انت مو بتيم.")
        owner = int(r.get(f"team:{my_team_id}:owner") or 0)
        if owner != user_id:
            return m.reply(f"{k} الاستلام لمالك التيم فقط.")

        curr_date = get_daily_key()

        if r.get(f"team:{my_team_id}:task_claimed:{curr_date}"):
            return m.reply(f"✅ استلمتوا جائزة اليوم خلاص! تعالوا بكرة.")

        daily_wins = int(r.get(f"team:{my_team_id}:daily_wins:{curr_date}") or 0)
        if daily_wins < 3:
            return m.reply(f"❌ ما خلصتوا المهام بعد! تحتاجون {3 - daily_wins} فوز/قصف ناجح إضافي.\nارسل `المهام` للتفاصيل.")

        # تم إكمال المهام - إعطاء الجائزة
        r.set(f"team:{my_team_id}:task_claimed:{curr_date}", 1, ex=86400)

        prize = random.choice(["floos", "pts", "cards", "soldiers", "missiles"])
        t_name = r.get(f"team:{my_team_id}:name") or "تيمك"

        if prize == "floos":
            reward_amount = random.choice([3000000, 5000000, 7000000, 10000000])
            r.set(f'{user_id}:Floos', int(r.get(f'{user_id}:Floos') or 0) + reward_amount)
            m.reply(f"🎁 **مبروك تيم « {t_name} »!**\n\n🏆 جائزة المهام: **{reward_amount:,}** ريال انضافت لرصيد المالك! 💸")
        elif prize == "pts":
            pts_reward = random.choice([50, 100, 150, 200])
            r.set(f"team:{my_team_id}:points", int(r.get(f"team:{my_team_id}:points") or 0) + pts_reward)
            m.reply(f"🎁 **مبروك تيم « {t_name} »!**\n\n🏆 جائزة المهام: **{pts_reward}** نقطة تيم إضافية! 💎")
        elif prize == "cards":
            card_type = random.choice(["skip_time", "name_change", "invite_change"])
            card_names = {"skip_time": "تجاوز الوقت", "name_change": "تغيير الاسم", "invite_change": "تغيير الرمز"}
            my_cards = int(r.get(f"user_cards:{user_id}:{card_type}") or 0)
            r.set(f"user_cards:{user_id}:{card_type}", my_cards + 1)
            m.reply(f"🎁 **مبروك تيم « {t_name} »!**\n\n🏆 جائزة المهام: بطاقة **{card_names[card_type]}** نادرة! 💳")
        elif prize == "soldiers":
            sol_reward = random.choice([500, 1000, 2000, 3000])
            curr_sol = int(r.get(f"team:{my_team_id}:soldiers") or 0)
            r.set(f"team:{my_team_id}:soldiers", curr_sol + sol_reward)
            m.reply(f"🎁 **مبروك تيم « {t_name} »!**\n\n🏆 جائزة المهام: **{sol_reward:,}** جندي انضموا لتيمكم! 🪖")
        elif prize == "missiles":
            mis_reward = random.choice([5, 10, 15, 20])
            curr_mis = int(r.get(f"team:{my_team_id}:missiles") or 0)
            r.set(f"team:{my_team_id}:missiles", curr_mis + mis_reward)
            m.reply(f"🎁 **مبروك تيم « {t_name} »!**\n\n🏆 جائزة المهام: **{mis_reward}** صاروخ انضاف لعتادكم! 🚀")

    # =====================================================
    #                 توب الغزاه
    # =====================================================
    if text == "توب الغزاه" or text == "توب الغزاة":
        teams = r.smembers("AllTeamsList")
        if not teams:
            return m.reply(f"{k} لا يوجد تيمات حالياً.")

        team_data = []
        for t in teams:
            tid = safe_str(t)
            pts = int(r.get(f"team:{tid}:points") or 0)
            name = r.get(f"team:{tid}:name")
            visible = r.get(f"team:{tid}:visible")
            m_count = r.scard(f"team:{tid}:members")
            if name:
                team_data.append({
                    "name": safe_str(name),
                    "pts": pts,
                    "visible": visible,
                    "members": m_count,
                    "tid": tid
                })

        if not team_data:
            return m.reply(f"{k} لا يوجد تيمات بتصنيف حالياً.")

        top = sorted(team_data, key=lambda x: x["pts"], reverse=True)

        # تقسيم حسب المستويات
        txt = "🏴 **تــوب التيمــات (الغـــزاة):**\n\n"

        # ماسي
        diamond = [t for t in top if get_team_level_rank(t['pts']) == 4]
        if diamond:
            txt += "💎 **ماسي 🥇:**\n"
            for i, td in enumerate(diamond[:5], 1):
                vis_icon = "👁" if td['visible'] else "👻"
                txt += f"  {i}. {td['name']} | 💎{td['pts']:,} | 👥{td['members']} {vis_icon}\n"
            txt += "\n"

        # فضي
        silver = [t for t in top if get_team_level_rank(t['pts']) == 3]
        if silver:
            txt += "🥈 **فضي:**\n"
            for i, td in enumerate(silver[:5], 1):
                vis_icon = "👁" if td['visible'] else "👻"
                txt += f"  {i}. {td['name']} | 💎{td['pts']:,} | 👥{td['members']} {vis_icon}\n"
            txt += "\n"

        # برونزي
        bronze = [t for t in top if get_team_level_rank(t['pts']) == 2]
        if bronze:
            txt += "🥉 **برونزي:**\n"
            for i, td in enumerate(bronze[:5], 1):
                vis_icon = "👁" if td['visible'] else "👻"
                txt += f"  {i}. {td['name']} | 💎{td['pts']:,} | 👥{td['members']} {vis_icon}\n"
            txt += "\n"

        # ضعيف
        weak = [t for t in top if get_team_level_rank(t['pts']) == 1]
        if weak:
            txt += "⬇️ **ضعيف:**\n"
            for i, td in enumerate(weak[:5], 1):
                vis_icon = "👁" if td['visible'] else "👻"
                txt += f"  {i}. {td['name']} | 💎{td['pts']:,} | 👥{td['members']} {vis_icon}\n"

        # معلومات تيم المرسل
        if my_team_id:
            my_pts_val = int(r.get(f"team:{my_team_id}:points") or 0)
            my_t_name = r.get(f"team:{my_team_id}:name") or "تيمك"
            txt += f"\n━━━━━━━━━\n🏴 **تيمك:** {my_t_name} | 💎{my_pts_val:,} | {get_team_level(my_pts_val)}"

        m.reply(txt)

    # =====================================================
    #         أوامر مساعدة - قائمة أوامر الغزاة
    # =====================================================
    if text in ["اوامر الغزاه", "اوامر الغزاة", "أوامر الغزاة", "أوامر الغزاه", "قائمة الغزاة"]:
        m.reply(f"""🏴 **أوامر لعبة الغزاة (التيمات):**

━━━ **إنشاء وإدارة التيم** ━━━
📌 `انشاء تيم [الاسم]` - إنشاء تيم (20 مليون)
🗑 `مسح تيمي` - مسح التيم بالكامل
ℹ️ `معلومات تيمي` - رمز الدعوة والهجوم (للمالك)
📊 `عتادي` أو `تيمي` - معلومات التيم والعتاد
👥 `اعضاء التيم` - عرض الأعضاء

━━━ **دخول وخروج** ━━━
🚪 `دخول التيم [الرمز]` - الانضمام لتيم
🚶 `خروج من التيم` - مغادرة التيم
🔒 `قفل دخول التيم` / `فتح دخول التيم`

━━━ **الإدارة** ━━━
👢 `طرد [آيدي/رد]` - طرد عضو
🚫 `حظر [آيدي/رد]` - طرد وحظر عضو
👁 `اظهار تيمي` / `اخفاء تيمي`
🔒 `قفل الهجوم` / `فتح الهجوم`

━━━ **المتاجر** ━━━
🛒 `متجر الغزاه` - شراء العتاد
🌍 `المتجر العالمي` - بطاقات محدودة
💳 `استخدام البطائق` - عرض بطاقاتك

━━━ **الحرب** ━━━
⚔️ `هجوم [رمز]` - الهجوم على تيم
💣 `قصف [رمز]` - قصف تيم بصاروخ

━━━ **أخرى** ━━━
📋 `المهام` أو `مهام التيم` - المهام اليومية
🎁 `جائزة المهام` - استلام جائزة المهام
🏆 `توب الغزاه` - ترتيب التيمات
""")
