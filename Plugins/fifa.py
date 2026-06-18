import random, re, time, asyncio
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import r, Dev_Zaid, botUsername
from helpers.Ranks import *
from helpers.games import words

# ======================== مساعدات ========================

def get_club_level(points):
    if points >= 5000: return "أسطوري 🏆"
    elif points >= 2000: return "محترف 🥇"
    elif points >= 500: return "هاوي 🥈"
    else: return "مبتدئ 🥉"

def safe_str(val):
    if val is None:
        return None
    if isinstance(val, bytes):
        return val.decode('utf-8')
    return str(val)

# ======================== معالج اللعبة ========================

@Client.on_message(filters.text & filters.group, group=130)
def fifa_game_handler(c, m):
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
    
    # التحقق من وجود منافسة كتابة قيد الانتظار
    if r.get(f"fifa_typing:{m.chat.id}:active"):
        target_word = r.get(f"fifa_typing:{m.chat.id}:word")
        player1 = int(r.get(f"fifa_typing:{m.chat.id}:p1") or 0)
        player2 = int(r.get(f"fifa_typing:{m.chat.id}:p2") or 0)
        
        if text.strip() == target_word and user_id in [player1, player2]:
            r.delete(f"fifa_typing:{m.chat.id}:active")
            r.delete(f"fifa_typing:{m.chat.id}:word")
            
            # الفائز يحصل على نقاط ومهارات
            pts_reward = random.randint(10, 30)
            skills_reward = random.randint(5, 15)
            
            curr_pts = int(r.get(f"fifa:{user_id}:points") or 0)
            curr_skills = int(r.get(f"fifa:{user_id}:skills") or 0)
            
            if r.get(f"fifa:{user_id}:name"): # فقط إذا كان عنده نادي
                r.set(f"fifa:{user_id}:points", curr_pts + pts_reward)
                r.set(f"fifa:{user_id}:skills", curr_skills + skills_reward)
                m.reply(f"🎉 **اسسسسسسطورة!**\nاللاعب {m.from_user.mention} كان الأسرع!\n\nكسب ناديك:\n💎 {pts_reward} نقطة\n⚡️ {skills_reward} مهارة")
            else:
                m.reply(f"🎉 **اسسسسسسطورة!**\nاللاعب {m.from_user.mention} كان الأسرع!\n(لكن ليس لديك نادي لإضافة الجوائز إليه، ارسل `انشاء نادي` لتستفيد).")
            return

    # =====================================================
    #                    لعبة النوادي
    # =====================================================
    if text == "النوادي":
        m.reply(f"""⚽️ **لعبة النوادي (فيفا):**

أنشئ ناديك وطور لاعبينك ونافس على البطولات!

🔹 `انشاء نادي` ← لإنشاء نادي جديد (5,000,000 ريال)
🔹 `نادي` ← لعرض تفاصيل ناديك
🔹 `تدريب` ← لتدريب لاعبينك
🔹 `شراء لاعبين [العدد]` ← للتعاقد مع لاعبين جدد
🔹 `ضربة جزاء` ← للعب ضربة جزاء وكسب نقاط
🔹 `مباراة ودية` ← للعب مباراة ودية
🔹 `مباراة` ← لمباراة ضد خصم (بالرد)
🔹 `تنافس` ← لمنافسة سرعة كتابة (بالرد)
🔹 `توب النوادي` ← لعرض أقوى النوادي
🔹 `انضمام للدوري` ← للمشاركة في دوري الأبطال
""")
        return

    # =====================================================
    #                    انشاء نادي
    # =====================================================
    if text == "انشاء نادي":
        if r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} عندك نادي بالفعل! اسمه « {r.get(f'fifa:{user_id}:name')} »")

        r.set(f"fifa_setup:{user_id}", 1, ex=120)
        m.reply(f"⚽️ أهلاً بك في عالم كرة القدم!\nارسل الآن اسم ناديك الجديد (مثال: `نادي الهلال`)")
        return

    if r.get(f"fifa_setup:{user_id}"):
        if len(text) > 25:
            return m.reply(f"{k} اسم النادي طويل جداً! اختر اسم أقصر.")
            
        floos = int(r.get(f'{user_id}:Floos') or 0)
        cost = 5000000 # 5 مليون
        
        if floos < cost:
            r.delete(f"fifa_setup:{user_id}")
            return m.reply(f"❌ فلوسك ماتكفي لإنشاء النادي!\nتحتاج 5,000,000 ريال وأنت معك {floos:,} ريال.")
            
        r.set(f'{user_id}:Floos', floos - cost)
        r.delete(f"fifa_setup:{user_id}")
        
        r.set(f"fifa:{user_id}:name", text)
        r.set(f"fifa:{user_id}:players", 11)
        r.set(f"fifa:{user_id}:points", 0)
        r.set(f"fifa:{user_id}:skills", 50)
        r.sadd("FifaClubs", user_id)
        
        m.reply(f"🎊 **مبروك!** تم إنشاء نادي « {text} » بنجاح وتم خصم 5,000,000 ريال من رصيدك.\n\nتم منحك 11 لاعب أساسي ومهارة ابتدائية 50.\nارسل `نادي` لعرض تفاصيل فريقك.")
        return

    # =====================================================
    #                    تغير النادي
    # =====================================================
    if text == "تغير النادي" or text == "تغيير النادي":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي عشان تغيره!")
            
        r.set(f"fifa_change:{user_id}", 1, ex=120)
        m.reply(f"⚠️ **تنبيه:** تغيير النادي سيكلفك 2,000,000 ريال وسيتم تصفير عدد لاعبيك الاحتياطيين.\nإذا كنت متأكد، ارسل الاسم الجديد للنادي.")
        return

    if r.get(f"fifa_change:{user_id}"):
        floos = int(r.get(f'{user_id}:Floos') or 0)
        cost = 2000000
        if floos < cost:
            r.delete(f"fifa_change:{user_id}")
            return m.reply(f"❌ فلوسك ماتكفي!")
            
        r.set(f'{user_id}:Floos', floos - cost)
        r.delete(f"fifa_change:{user_id}")
        
        r.set(f"fifa:{user_id}:name", text)
        r.set(f"fifa:{user_id}:players", 11) # ريسيت للاعبين
        m.reply(f"✅ تم تغيير اسم ناديك إلى « {text} » بنجاح وتم خصم 2,000,000 ريال وتصفير اللاعبين الإضافيين.")
        return

    # =====================================================
    #                    حذف النادي
    # =====================================================
    if text == "حذف النادي":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        for key in r.keys(f"fifa:{user_id}:*"):
            r.delete(key)
        r.srem("FifaClubs", user_id)
        r.srem("FifaLeagueQueue", user_id)
        
        m.reply(f"🗑 تم حذف ناديك بالكامل، وتسريح جميع اللاعبين.")

    # =====================================================
    #                       نادي
    # =====================================================
    if text == "نادي":
        club_name = r.get(f"fifa:{user_id}:name")
        if not club_name:
            return m.reply(f"{k} ماعندك نادي! ارسل `انشاء نادي`.")
            
        players = int(r.get(f"fifa:{user_id}:players") or 11)
        points = int(r.get(f"fifa:{user_id}:points") or 0)
        skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        
        level = get_club_level(points)
        
        m.reply(f"""⚽️ **نادي « {club_name} »**
        
🔰 **المستوى:** {level}
💎 **نقاط النادي:** {points:,}
⚡️ **المهارات (التناغم):** {skills}
🏃‍♂️ **عدد اللاعبين:** {players}

💡 أوامر مفيدة: `تدريب`، `شراء لاعبين`، `مباراة ودية`، `ضربة جزاء`.
""")

    # =====================================================
    #                    شراء لاعبين
    # =====================================================
    if text.startswith("شراء لاعبين"):
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        parts = text.split()
        if len(parts) < 3:
            return m.reply(f"🛒 **سوق الانتقالات:**\nسعر اللاعب الواحد = 1,000,000 ريال\nكل لاعب يزيد من قوة مهارات فريقك.\n\nللشراء ارسل: `شراء لاعبين [العدد]`")
            
        try: amount = int(parts[2])
        except: return m.reply(f"❌ العدد غير صحيح.")
        
        if amount <= 0: return m.reply(f"❌ العدد يجب أن يكون أكبر من صفر.")
        
        cost = amount * 1000000
        floos = int(r.get(f'{user_id}:Floos') or 0)
        if floos < cost:
            return m.reply(f"❌ فلوسك ماتكفي! تحتاج {cost:,} ريال.")
            
        r.set(f'{user_id}:Floos', floos - cost)
        
        curr_players = int(r.get(f"fifa:{user_id}:players") or 11)
        curr_skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        
        r.set(f"fifa:{user_id}:players", curr_players + amount)
        r.set(f"fifa:{user_id}:skills", curr_skills + (amount * 2)) # كل لاعب يعطي 2 مهارة
        
        m.reply(f"✅ تم التعاقد مع **{amount}** لاعبين بنجاح!\n💸 تم خصم {cost:,} ريال.\n⚡️ مهارات ناديك زادت بمقدار {amount * 2}.")

    # =====================================================
    #                       تدريب
    # =====================================================
    if text == "تدريب":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        if r.get(f"fifa_train:{user_id}"):
            get = r.ttl(f"fifa_train:{user_id}")
            wait = time.strftime('%M:%S', time.gmtime(get))
            return m.reply(f"⏳ اللاعبين مجهدين من التدريب! انتظر {wait} دقيقة.")
            
        r.set(f"fifa_train:{user_id}", 1, ex=1200) # 20 دقيقة
        
        skill_gain = random.randint(3, 10)
        curr_skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        r.set(f"fifa:{user_id}:skills", curr_skills + skill_gain)
        
        m.reply(f"🏃‍♂️ **تدريب ناجح!**\nتطور تناغم الفريق واكتسبوا {skill_gain} مهارة إضافية.\n⚡️ مهاراتك الحالية: {curr_skills + skill_gain}")

    # =====================================================
    #                    ضربة جزاء
    # =====================================================
    if text == "ضربة جزاء":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        if r.get(f"fifa_penalty:{user_id}"):
            get = r.ttl(f"fifa_penalty:{user_id}")
            wait = time.strftime('%M:%S', time.gmtime(get))
            return m.reply(f"⏳ اللاعبون يتدربون على التسديد، عد بعد {wait} دقيقة.")
            
        r.set(f"fifa_penalty:{user_id}", 1, ex=300) # 5 دقائق
        
        skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        win_chance = min(85, max(30, skills // 10)) # نسبة الفوز بين 30% و 85%
        
        if random.randint(1, 100) <= win_chance:
            pts_gain = random.randint(10, 50)
            curr_pts = int(r.get(f"fifa:{user_id}:points") or 0)
            r.set(f"fifa:{user_id}:points", curr_pts + pts_gain)
            m.reply(f"🥅 ⚽️ **قووووووووول!**\nضربة جزاء أسطورية سكنت الشباك!\n💎 كسب ناديك {pts_gain} نقطة.")
        else:
            m.reply(f"🥅 🚫 **ضاعت!**\nالحارس تصدى للكرة ببراعة.. حاول مرة أخرى لاحقاً.")

    # =====================================================
    #                    مباراة ودية
    # =====================================================
    if text == "مباراة ودية":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        if r.get(f"fifa_friendly:{user_id}"):
            get = r.ttl(f"fifa_friendly:{user_id}")
            wait = time.strftime('%H:%M:%S', time.gmtime(get))
            return m.reply(f"⏳ فريقك مجهد، انتظر {wait} لترتيب مباراة ودية أخرى.")
            
        r.set(f"fifa_friendly:{user_id}", 1, ex=1800) # 30 دقيقة
        
        skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        
        if random.choice([True, False]):
            skill_gain = random.randint(10, 25)
            r.set(f"fifa:{user_id}:skills", skills + skill_gain)
            m.reply(f"🏆 **نهاية المباراة!**\nفاز فريقك بأداء رائع واكتسب اللاعبون خبرة.\n⚡️ مهارات ناديك زادت بمقدار {skill_gain}.")
        else:
            skill_loss = random.randint(5, 15)
            r.set(f"fifa:{user_id}:skills", max(10, skills - skill_loss))
            m.reply(f"❌ **هزيمة..**\nأداء سيء من الفريق وأخطاء دفاعية كارثية.\n📉 انخفضت مهارات ناديك بمقدار {skill_loss}.")

    # =====================================================
    #                    تنافس (بالرد)
    # =====================================================
    if text == "تنافس" and m.reply_to_message and m.reply_to_message.from_user:
        target_id = m.reply_to_message.from_user.id
        if target_id == user_id:
            return m.reply(f"تبي تتنافس مع نفسك؟ 😂")
            
        if r.get(f"fifa_typing:{m.chat.id}:active"):
            return m.reply(f"⏳ فيه منافسة شغالة حالياً بالقروب! انتظر لين تخلص.")
            
        word = random.choice(words)
        r.set(f"fifa_typing:{m.chat.id}:active", 1, ex=60)
        r.set(f"fifa_typing:{m.chat.id}:word", word, ex=60)
        r.set(f"fifa_typing:{m.chat.id}:p1", user_id, ex=60)
        r.set(f"fifa_typing:{m.chat.id}:p2", target_id, ex=60)
        
        m.reply(f"🏁 **منافسة سرعة بين {m.from_user.mention} و {m.reply_to_message.from_user.mention}**\n\nأول واحد يكتب هذه الكلمة بشكل صحيح يربح:\n\n`{word}`\n\nلديكما دقيقة واحدة!")

    # =====================================================
    #                    مباراة (بالرد)
    # =====================================================
    if text == "مباراة" and m.reply_to_message and m.reply_to_message.from_user:
        target_id = m.reply_to_message.from_user.id
        if target_id == user_id:
            return m.reply(f"ما تقدر تلعب مباراة ضد نفسك!")
            
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
        if not r.get(f"fifa:{target_id}:name"):
            return m.reply(f"❌ خصمك ماعنده نادي!")
            
        # التحقق من وقت الانتظار للمباراة الخاصة
        if r.get(f"fifa_pvp:{user_id}"):
            get = r.ttl(f"fifa_pvp:{user_id}")
            wait = time.strftime('%M:%S', time.gmtime(get))
            return m.reply(f"⏳ فريقك مرهق من المباريات! انتظر {wait} دقيقة.")
            
        r.set(f"fifa_pvp:{user_id}", 1, ex=600) # 10 دقائق
        
        my_club = r.get(f"fifa:{user_id}:name")
        his_club = r.get(f"fifa:{target_id}:name")
        
        my_skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        his_skills = int(r.get(f"fifa:{target_id}:skills") or 50)
        
        # إضافة حظ بسيط
        my_power = my_skills * random.uniform(0.8, 1.2)
        his_power = his_skills * random.uniform(0.8, 1.2)
        
        if my_power > his_power:
            # الفائز
            pts_gain = random.randint(20, 60)
            skills_gain = random.randint(5, 15)
            
            my_pts = int(r.get(f"fifa:{user_id}:points") or 0)
            r.set(f"fifa:{user_id}:points", my_pts + pts_gain)
            r.set(f"fifa:{user_id}:skills", my_skills + skills_gain)
            
            # الخاسر ينقص مهاراته قليل
            r.set(f"fifa:{target_id}:skills", max(10, his_skills - random.randint(2, 5)))
            
            m.reply(f"""🏆 **صافرة النهاية!**
            
نادي {my_club} 🆚 نادي {his_club}
✅ **الفائز:** {my_club}

💎 حصل النادي الفائز على {pts_gain} نقطة و {skills_gain} مهارة.
""")
        else:
            # الخسارة
            pts_gain = random.randint(20, 60)
            skills_gain = random.randint(5, 15)
            
            his_pts = int(r.get(f"fifa:{target_id}:points") or 0)
            r.set(f"fifa:{target_id}:points", his_pts + pts_gain)
            r.set(f"fifa:{target_id}:skills", his_skills + skills_gain)
            
            r.set(f"fifa:{user_id}:skills", max(10, my_skills - random.randint(2, 5)))
            
            m.reply(f"""🏆 **صافرة النهاية!**
            
نادي {my_club} 🆚 نادي {his_club}
❌ **الفائز:** {his_club}

💎 حصل الخصم على {pts_gain} نقطة و {skills_gain} مهارة.
📉 مهارات ناديك انخفضت بسبب الأداء السيء.
""")

    # =====================================================
    #                 الانضمام للدوري
    # =====================================================
    if text == "انضمام للدوري":
        if not r.get(f"fifa:{user_id}:name"):
            return m.reply(f"{k} ماعندك نادي!")
            
        if r.sismember("FifaLeagueQueue", user_id):
            return m.reply(f"✅ أنت مسجل في الدوري بالفعل، بانتظار القرعة والمباريات.")
            
        my_pts = int(r.get(f"fifa:{user_id}:points") or 0)
        my_skills = int(r.get(f"fifa:{user_id}:skills") or 50)
        
        if my_pts < 30 or my_skills < 30:
            return m.reply(f"❌ رسوم الانضمام للدوري هي 30 نقطة و 30 مهارة، وأنت لا تملك ما يكفي.")
            
        r.set(f"fifa:{user_id}:points", my_pts - 30)
        r.set(f"fifa:{user_id}:skills", my_skills - 30)
        
        r.sadd("FifaLeagueQueue", user_id)
        
        m.reply(f"🏆 تم تسجيل ناديك في دوري الأبطال!\nتم خصم 30 نقطة و 30 مهارة رسوم الاشتراك.\nانتظر القرعة والمباريات (يتم سحب الدوري تلقائياً كل ساعة بمجرد اكتمال 10 نوادي).")

    # =====================================================
    #                  توب النوادي
    # =====================================================
    if text == "توب النوادي":
        clubs = r.smembers("FifaClubs")
        if not clubs:
            return m.reply(f"لا توجد نوادي حالياً.")
            
        data = []
        for uid in clubs:
            uid = safe_str(uid)
            name = r.get(f"fifa:{uid}:name")
            pts = int(r.get(f"fifa:{uid}:points") or 0)
            if name:
                data.append({"name": safe_str(name), "pts": pts})
                
        if not data:
            return m.reply(f"لا توجد نوادي حالياً.")
            
        top = sorted(data, key=lambda x: x["pts"], reverse=True)
        
        txt = "🏆 **تــوب النــوادي (فيفا):**\n\n"
        for i, club in enumerate(top[:20], 1):
            emoji = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}-'
            lvl = get_club_level(club["pts"])
            txt += f"{emoji} {club['name']} | 💎 {club['pts']:,} | {lvl}\n"
            
        m.reply(txt)

# ======================== تاسك الدوري ========================
# هذا التاسك يتم تشغيله في main.py

async def fifa_league_task(app):
    while True:
        try:
            # تحقق كل 5 دقائق
            await asyncio.sleep(300)
            
            queue = r.smembers("FifaLeagueQueue")
            if len(queue) >= 10:
                # سحب 10 نوادي بشكل عشوائي
                selected_clubs = random.sample(list(queue), 10)
                
                # ترتيبهم كمواجهات (5 مباريات)
                matches = [(selected_clubs[i], selected_clubs[i+1]) for i in range(0, 10, 2)]
                
                # تنظيفهم من طابور الانتظار
                for u in selected_clubs:
                    r.srem("FifaLeagueQueue", u)
                
                # لعب المباريات
                for p1, p2 in matches:
                    p1 = safe_str(p1)
                    p2 = safe_str(p2)
                    
                    p1_skills = int(r.get(f"fifa:{p1}:skills") or 50)
                    p2_skills = int(r.get(f"fifa:{p2}:skills") or 50)
                    
                    p1_power = p1_skills * random.uniform(0.7, 1.3)
                    p2_power = p2_skills * random.uniform(0.7, 1.3)
                    
                    p1_pts = int(r.get(f"fifa:{p1}:points") or 0)
                    p2_pts = int(r.get(f"fifa:{p2}:points") or 0)
                    
                    # خصم الدخول كان 30 نقطة، الجائزة للمنتصر الدبل (60 نقطة)
                    reward = 60
                    
                    diff = abs(p1_power - p2_power)
                    
                    if diff < 5:
                        # تعادل
                        r.set(f"fifa:{p1}:points", p1_pts + 30)
                        r.set(f"fifa:{p2}:points", p2_pts + 30)
                        # نرسل اشعارات
                        await safe_send(app, p1, f"🏆 **دوري الأبطال:**\nانتهت مباراتك بالتعادل. تم استرجاع نقاطك (30).")
                        await safe_send(app, p2, f"🏆 **دوري الأبطال:**\nانتهت مباراتك بالتعادل. تم استرجاع نقاطك (30).")
                    elif p1_power > p2_power:
                        # فوز p1
                        r.set(f"fifa:{p1}:points", p1_pts + reward)
                        await safe_send(app, p1, f"🏆 **دوري الأبطال:**\nانتصصصصار! سحق فريقك الخصم في الدوري واسترجعت الدبل (60 نقطة)! 🎉")
                        await safe_send(app, p2, f"🏆 **دوري الأبطال:**\nهزيمة قاسية في الدوري.. خسرت رسوم الدخول وحظاً أوفر المرة القادمة. 💔")
                    else:
                        # فوز p2
                        r.set(f"fifa:{p2}:points", p2_pts + reward)
                        await safe_send(app, p2, f"🏆 **دوري الأبطال:**\nانتصصصصار! سحق فريقك الخصم في الدوري واسترجعت الدبل (60 نقطة)! 🎉")
                        await safe_send(app, p1, f"🏆 **دوري الأبطال:**\nهزيمة قاسية في الدوري.. خسرت رسوم الدخول وحظاً أوفر المرة القادمة. 💔")
                        
        except Exception as e:
            # صمت الأخطاء لتجنب إيقاف التاسك
            pass

async def safe_send(app, user_id, text):
    try:
        await app.send_message(int(user_id), text)
    except:
        pass
