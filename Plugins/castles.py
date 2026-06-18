import random, re, time
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import r, Dev_Zaid, botUsername
from helpers.Ranks import admin_pls

def get_top_castles(users):
    users = [tuple(i.items()) for i in users]
    top = sorted(users, key=lambda i: i[-1][-1], reverse=True)
    top = [dict(i) for i in top]
    return top

def get_emoji_rank(count):
    if count == 1: return '🥇'
    elif count == 2: return '🥈'
    elif count == 3: return '🥉'
    else: return f'{count} -'

@Client.on_message(filters.text & filters.group, group=120)
def castles_game_handler(c, m):
    if not getattr(m, 'from_user', None): return
    if r.get(f'{m.chat.id}:disableGames:{Dev_Zaid}'): return
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'): return
    if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'): return
    
    k = r.get(f'{Dev_Zaid}:botkey') or '⇜'
    text = m.text
    name = r.get(f'{Dev_Zaid}:BotName') or 'اتاك'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    # --- لعبة قلاع ---
    if text == "القلاع" or text == "قلاع":
        m.reply(f"""🏰 **لعبة القلاع:**

أنشئ قلعتك وطورها واجمع الموارد وحارب الحكام الآخرين!

🔹 `انشاء قلعه` ← لإنشاء قلعتك
🔹 `قلعتي` ← لعرض تفاصيل قلعتك
🔹 `مواردي` ← لعرض مخزن الموارد
🔹 `متجر الموارد` ← لشراء الموارد
🔹 `تطوير قلعتي` ← لتطوير مستوى القلعة
🔹 `انشاء معسكر` ← لإنشاء معسكر جيش
🔹 `بحث الكنز` ← للبحث عن كنوز
🔹 `مبارزه` ← لمبارزة حاكم آخر (بالرد)
🔹 `توب الحكام` ← لعرض أقوى القلاع
""")
        return

    # --- إنشاء قلعه ---
    if text == "انشاء قلعه":
        if r.get(f"{m.from_user.id}:castle_level"):
            return m.reply(f"{k} عندك قلعة بالفعل بمستوى {r.get(f'{m.from_user.id}:castle_level')} 🏰")
        
        r.set(f"{m.from_user.id}:castle_level", 1)
        r.set(f"{m.from_user.id}:castle_wood", 0)
        r.set(f"{m.from_user.id}:castle_stone", 0)
        r.set(f"{m.from_user.id}:castle_iron", 0)
        r.set(f"{m.from_user.id}:castle_gold", 0)
        r.set(f"{m.from_user.id}:castle_points", 100)
        r.sadd('CastlesList', m.from_user.id)
        
        return m.reply(f"🏰 {k} مبروك! تم إنشاء قلعتك بنجاح\n🎁 حصلت على 100 نقطة حكام كبداية.\nلمعرفة التفاصيل ارسل `قلعتي`")

    # --- قلعتي ---
    if text == "قلعتي":
        if not r.get(f"{m.from_user.id}:castle_level"):
            return m.reply(f"{k} ماعندك قلعة! ارسل `انشاء قلعه` عشان تبدأ.")
        
        level = int(r.get(f"{m.from_user.id}:castle_level") or 1)
        pts = int(r.get(f"{m.from_user.id}:castle_points") or 0)
        army = int(r.get(f"{m.from_user.id}:castle_army") or 0)
        army_strength = army // 1000
        
        m.reply(f"""🏰 **قلعة الحاكم:** {m.from_user.mention}
        
🔰 **مستوى القلعة:** {level}
💎 **نقاط الحكام:** {pts:,}
⚔️ **الجيش:** {army:,} جندي (قوة: {army_strength})

للتطوير ارسل `تطوير قلعتي`
لرؤية الموارد ارسل `مواردي`
""")

    # --- مواردي ---
    if text == "مواردي":
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} ماعندك قلعة! ارسل `انشاء قلعه`")
        
        wood = int(r.get(f"{m.from_user.id}:castle_wood") or 0)
        stone = int(r.get(f"{m.from_user.id}:castle_stone") or 0)
        iron = int(r.get(f"{m.from_user.id}:castle_iron") or 0)
        gold = int(r.get(f"{m.from_user.id}:castle_gold") or 0)
        
        m.reply(f"""📦 **مخزن الموارد الخاص بك:**
        
🪵 **خشب:** {wood:,}
🪨 **حجر:** {stone:,}
⛓ **حديد:** {iron:,}
🪙 **ذهب:** {gold:,}

لشراء المزيد ارسل `متجر الموارد`
""")

    # --- متجر الموارد ---
    if text == "متجر الموارد":
        m.reply(f"""🏪 **متجر الموارد:**
        
اسعار الموارد بنقاط الحكام:
🪵 **خشب:** 3 خشب = 1 نقطة
🪨 **حجر:** 3 حجر = 1 نقطة
⛓ **حديد:** 3 حديد = 1 نقطة
🪙 **ذهب:** 1 ذهب = 1 نقطة

طريقة الشراء:
`شراء موارد خشب 30`
(سيتم خصم 10 نقاط واعطائك 30 خشب)
""")

    # --- شراء موارد ---
    if text.startswith("شراء موارد ") and len(text.split()) == 4:
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} ماعندك قلعة!")
        
        parts = text.split()
        res_type = parts[2]
        try:
            amount = int(parts[3])
        except:
            return m.reply(f"{k} الكمية يجب أن تكون أرقام!")
        
        if amount <= 0: return m.reply(f"{k} حدد كمية صحيحة!")
        
        pts = int(r.get(f"{m.from_user.id}:castle_points") or 0)
        
        if res_type == "ذهب":
            cost = amount
            res_key = "castle_gold"
        elif res_type in ["خشب", "حجر", "حديد"]:
            cost = amount // 3
            if amount % 3 != 0: cost += 1 # جبر الكسر
            if res_type == "خشب": res_key = "castle_wood"
            elif res_type == "حجر": res_key = "castle_stone"
            elif res_type == "حديد": res_key = "castle_iron"
        else:
            return m.reply(f"{k} المورد غير موجود (خشب، حجر، حديد، ذهب)")
            
        if pts < cost:
            return m.reply(f"{k} نقاطك ماتكفي! تحتاج {cost} نقطة لشراء هذه الكمية.")
            
        # Limit per day
        daily_limit_key = f"{m.from_user.id}:castle_daily_buy"
        bought_today = int(r.get(daily_limit_key) or 0)
        if bought_today + amount > 1000:
            return m.reply(f"{k} لقد وصلت للحد الأقصى للشراء اليومي المسموح (1000 مورد).")
            
        r.set(daily_limit_key, bought_today + amount, ex=86400)
        r.set(f"{m.from_user.id}:castle_points", pts - cost)
        
        curr_res = int(r.get(f"{m.from_user.id}:{res_key}") or 0)
        r.set(f"{m.from_user.id}:{res_key}", curr_res + amount)
        
        m.reply(f"{k} تم شراء {amount} {res_type} بنجاح ✅\nالنقاط المخصومة: {cost} نقطة.")

    # --- تطوير قلعتي ---
    if text == "تطوير قلعتي":
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} ماعندك قلعة!")
        
        if r.get(f"{m.from_user.id}:castle_upgrade_wait"):
            get = r.ttl(f"{m.from_user.id}:castle_upgrade_wait")
            wait = time.strftime('%H:%M:%S', time.gmtime(get))
            return m.reply(f"⏳ قلعتك تحت التطوير! تكتمل بعد {wait}")
            
        level = int(r.get(f"{m.from_user.id}:castle_level") or 1)
        req_wood = level * 100
        req_stone = level * 100
        req_iron = level * 50
        req_gold = level * 10
        
        wood = int(r.get(f"{m.from_user.id}:castle_wood") or 0)
        stone = int(r.get(f"{m.from_user.id}:castle_stone") or 0)
        iron = int(r.get(f"{m.from_user.id}:castle_iron") or 0)
        gold = int(r.get(f"{m.from_user.id}:castle_gold") or 0)
        
        if wood < req_wood or stone < req_stone or iron < req_iron or gold < req_gold:
            return m.reply(f"""❌ **مواردك غير كافية لتطوير القلعة لمستوى {level+1}**
            
متطلبات التطوير:
🪵 خشب: {req_wood}
🪨 حجر: {req_stone}
⛓ حديد: {req_iron}
🪙 ذهب: {req_gold}
""")
            
        r.set(f"{m.from_user.id}:castle_wood", wood - req_wood)
        r.set(f"{m.from_user.id}:castle_stone", stone - req_stone)
        r.set(f"{m.from_user.id}:castle_iron", iron - req_iron)
        r.set(f"{m.from_user.id}:castle_gold", gold - req_gold)
        
        upgrade_time = level * 600 # 10 mins per level
        r.set(f"{m.from_user.id}:castle_upgrade_wait", 1, ex=upgrade_time)
        r.set(f"{m.from_user.id}:castle_level", level + 1)
        
        wait_str = time.strftime('%H:%M:%S', time.gmtime(upgrade_time))
        m.reply(f"🛠 تم البدء بتطوير القلعة إلى مستوى {level+1}!\nسيكتمل التطوير بعد {wait_str}.")

    # --- انشاء معسكر ---
    if text == "انشاء معسكر" or text == "انشاء معكسر":
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} لازم تنشئ قلعة أولاً!")
        if r.get(f"{m.from_user.id}:castle_camp"): return m.reply(f"{k} عندك معسكر جيش بالفعل ⛺️")
        
        r.set(f"{m.from_user.id}:castle_camp", 1)
        r.set(f"{m.from_user.id}:castle_army", 0)
        m.reply(f"⛺️ تم إنشاء المعسكر بنجاح!\nالآن يمكنك `شراء جيش` وتطويره.")

    # --- شراء جيش ---
    if text.startswith("شراء جيش ") and len(text.split()) == 3:
        if not r.get(f"{m.from_user.id}:castle_camp"): return m.reply(f"{k} ماعندك معسكر! ارسل `انشاء معسكر`")
        
        try:
            amount = int(text.split()[2])
        except:
            return m.reply(f"{k} يجب أن يكون العدد أرقام.")
            
        if amount <= 0: return m.reply(f"{k} عدد غير صالح!")
        
        pts = int(r.get(f"{m.from_user.id}:castle_points") or 0)
        cost = amount // 10
        if amount % 10 != 0: cost += 1
        
        if pts < cost: return m.reply(f"{k} نقاطك ماتكفي! تحتاج {cost} نقطة لتدريب {amount} جندي.")
        
        r.set(f"{m.from_user.id}:castle_points", pts - cost)
        army = int(r.get(f"{m.from_user.id}:castle_army") or 0)
        r.set(f"{m.from_user.id}:castle_army", army + amount)
        
        m.reply(f"⚔️ تم تدريب وانضمام {amount} جندي لمعسكرك بنجاح!\nقوة جيشك ترتفع كلما جمعت 1000 جندي (ارسل `تطوير الجيش`).")

    # --- تطوير الجيش ---
    if text == "تطوير الجيش":
        if not r.get(f"{m.from_user.id}:castle_camp"): return m.reply(f"{k} ماعندك معسكر!")
        army = int(r.get(f"{m.from_user.id}:castle_army") or 0)
        strength = army // 1000
        m.reply(f"🛡 **قوة جيشك الحالية:** {strength} نقطة.\n(يتم احتساب نقطة قوة واحدة لكل 1000 جندي تلقائياً تفيدك في المبارزات).")

    # --- بحث الكنز ---
    if text == "بحث الكنز":
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} لازم تنشئ قلعة أولاً!")
        if r.get(f"{m.from_user.id}:castle_treasure_wait"):
            get = r.ttl(f"{m.from_user.id}:castle_treasure_wait")
            wait = time.strftime('%M:%S', time.gmtime(get))
            return m.reply(f"⏳ لا يمكنك البحث الآن. عد بعد {wait} دقيقة.")
            
        r.set(f"{m.from_user.id}:castle_treasure_wait", 1, ex=3600) # 1 hour
        
        chance = random.randint(1, 100)
        if chance <= 40: # 40% Resources
            res_type = random.choice(["wood", "stone", "iron", "gold"])
            amount = random.randint(50, 200)
            if res_type == "gold": amount = random.randint(10, 50)
            
            curr = int(r.get(f"{m.from_user.id}:castle_{res_type}") or 0)
            r.set(f"{m.from_user.id}:castle_{res_type}", curr + amount)
            
            name_ar = {"wood":"خشب", "stone":"حجر", "iron":"حديد", "gold":"ذهب"}[res_type]
            m.reply(f"🎉 **مبروك!** وجدت كنزاً يحتوي على {amount} {name_ar} 🎁")
            
        elif chance <= 70: # 30% Army
            amount = random.randint(100, 500)
            army = int(r.get(f"{m.from_user.id}:castle_army") or 0)
            r.set(f"{m.from_user.id}:castle_army", army + amount)
            m.reply(f"⚔️ **رهيب!** أثناء بحثك انضم إليك {amount} جندي متمرد وقرروا الانضمام لمعسكرك.")
            
        elif chance <= 80: # 10% Immunity
            cards = int(r.get(f"{m.from_user.id}:castle_immunity_cards") or 0)
            r.set(f"{m.from_user.id}:castle_immunity_cards", cards + 1)
            m.reply(f"🛡 **أسطوري!** لقد عثرت على **بطاقة حصانة**. يمكنك استخدامها بـ `تفعيل الحصانه` لحماية قلعتك.")
            
        else: # 20% Nothing
            m.reply(f"😔 للأسف رجعت من البحث خالي اليدين، حاول مجدداً بعد ساعة.")

    # --- الحصانة ---
    if text == "تفعيل الحصانه" or text == "تفعيل الحصانة":
        if r.get(f"{m.from_user.id}:castle_immunity_active"):
            return m.reply(f"🛡 حصانتك مفعلة بالفعل!")
        cards = int(r.get(f"{m.from_user.id}:castle_immunity_cards") or 0)
        if cards <= 0:
            return m.reply(f"❌ ماعندك بطاقات حصانة. جرب حظك في `بحث الكنز`.")
            
        r.set(f"{m.from_user.id}:castle_immunity_cards", cards - 1)
        r.set(f"{m.from_user.id}:castle_immunity_active", 1, ex=7200) # 2 hours
        m.reply(f"🛡 تم تفعيل الدرع والحصانة لمدة ساعتين. لن يستطيع أحد مهاجمتك!")
        
    if text == "تعطيل الحصانه" or text == "تعطيل الحصانة":
        if not r.get(f"{m.from_user.id}:castle_immunity_active"):
            return m.reply(f"🛡 حصانتك غير مفعلة أصلاً.")
        r.delete(f"{m.from_user.id}:castle_immunity_active")
        m.reply(f"🛡 تم إطفاء الدرع. انتبه قلعتك الآن في خطر!")

    if text == "حصانتي":
        if r.get(f"{m.from_user.id}:castle_immunity_active"):
            get = r.ttl(f"{m.from_user.id}:castle_immunity_active")
            wait = time.strftime('%H:%M:%S', time.gmtime(get))
            cards = int(r.get(f"{m.from_user.id}:castle_immunity_cards") or 0)
            m.reply(f"🛡 حصانتك مفعله وستنتهي بعد: {wait}\nلديك {cards} بطاقة حصانة في المخزون.")
        else:
            cards = int(r.get(f"{m.from_user.id}:castle_immunity_cards") or 0)
            m.reply(f"🛡 حصانتك غير مفعلة.\nلديك {cards} بطاقة حصانة في المخزون.")

    # --- المبارزة الفردية ---
    if text == "مبارزه" or text == "مبارزة":
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return m.reply(f"{k} هذا الأمر بالرد على الشخص اللي تبي تبارزه.")
            
        target_id = m.reply_to_message.from_user.id
        if target_id == m.from_user.id: return m.reply(f"{k} تبي تهاجم نفسك؟")
        
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} ماعندك قلعة!")
        if not r.get(f"{target_id}:castle_level"): return m.reply(f"{k} خصمك ماعنده قلعة.")
        
        if r.get(f"{target_id}:castle_immunity_active"):
            return m.reply(f"🛡 خصمك مفعل الحصانة، لا يمكنك مهاجمته!")
            
        my_army = int(r.get(f"{m.from_user.id}:castle_army") or 0)
        my_str = my_army // 1000
        
        his_army = int(r.get(f"{target_id}:castle_army") or 0)
        his_str = his_army // 1000
        
        if my_str == 0: return m.reply(f"❌ جيشك ضعيف جداً! تحتاج قوة جيش على الأقل 1 (1000 جندي) للمبارزة.")
        
        if my_str >= his_str:
            # Win
            loot_army = his_army // 10
            r.set(f"{target_id}:castle_army", his_army - loot_army)
            r.set(f"{m.from_user.id}:castle_army", my_army + loot_army)
            m.reply(f"⚔️ **انتصار!**\nقمت بسحق جيش الخصم وغنمت {loot_army} جندي انضموا لصفك!")
        else:
            # Lose
            loss_army = my_army // 5
            r.set(f"{m.from_user.id}:castle_army", my_army - loss_army)
            m.reply(f"💀 **هزيمة ساحقة!**\nجيش الخصم كان أقوى منك، فقدت {loss_army} جندي في المعركة.")

    # --- الانضمام للمبارزة العالمية وتوب الحكام ---
    if text == "الانضمام للمبارزه" or text == "الانضمام للمبارزة":
        if not r.get(f"{m.from_user.id}:castle_level"): return m.reply(f"{k} ماعندك قلعة!")
        if r.sismember("CastleGlobalDuel", m.from_user.id): return m.reply(f"✅ أنت منضم للمبارزة العالمية بالفعل.")
        
        r.sadd("CastleGlobalDuel", m.from_user.id)
        m.reply(f"⚔️ تم تسجيلك في المبارزة العالمية الكبرى! ارسل `المبارزين` لتشوف المشاركين.")
        
    if text == "المبارزين":
        if not r.smembers("CastleGlobalDuel"): return m.reply(f"لا يوجد أحد مسجل في المبارزة العالمية حالياً.")
        
        txt = "⚔️ **المشاركين في المبارزة العالمية:**\n\n"
        count = 1
        for u in r.smembers("CastleGlobalDuel"):
            user_id = int(u)
            try:
                name = c.get_users(user_id).first_name[:10]
            except:
                name = "غير معروف"
            txt += f"{count}- {name}\n"
            count += 1
        txt += f"\nستبدأ المبارزة تلقائياً عندما يقوم أحد الإداريين بإغلاق التسجيل."
        m.reply(txt)

    if text == "توب الحكام":
        if not r.smembers("CastlesList"): return m.reply(f"{k} لا توجد قلاع في المملكة بعد.")
        
        users = []
        for u in r.smembers("CastlesList"):
            user_id = int(u)
            level = int(r.get(f"{user_id}:castle_level") or 1)
            try:
                name = c.get_users(user_id).first_name[:10]
            except:
                name = "غير معروف"
            users.append({"name": name, "level": level})
            
        top = get_top_castles(users)
        txt = "🤴🏻 **تــوب الحـكـام (أقوى القلاع):**\n\n"
        count = 1
        for user in top:
            if count > 20: break
            emoji = get_emoji_rank(count)
            lvl = user["level"]
            name = user["name"]
            txt += f"**{emoji} القلعة:** مستوى {lvl} 🏰 | المالك: {name}\n"
            count += 1
            
        m.reply(txt)

    # --- التحالف ---
    if text.startswith("تحالف ") and len(text.split()) == 2:
        if not m.reply_to_message and not getattr(m, 'entities', None):
            return m.reply(f"🤝 منشن صديقك أو رد عليه لإرسال طلب تحالف.")
            
        m.reply(f"🤝 جاري إرسال طلب تحالف... (سيتم إضافة الميزة بالكامل في التحديث القادم بعد استقرار اللعبة).")
