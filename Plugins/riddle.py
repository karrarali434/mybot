import random
import time
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import r, Dev_Zaid

# مجموعة ألغاز متنوعة مع الخيارات والإجابة الصحيحة
riddles_data = [
    {"q": "ما هي الكلمه التي يفصل اولها عن اخرها ميل؟", "c": ["مدينة", "جميلة", "ولاية"], "a": "جميلة"},
    {"q": "شيء كلما أخذت منه كبر، فما هو؟", "c": ["الحفرة", "الجبل", "العمر"], "a": "الحفرة"},
    {"q": "ما هو الشيء الذي يمشي بلا رجلين ويبكي بلا عينين؟", "c": ["السحاب", "الرياح", "الظل"], "a": "السحاب"},
    {"q": "ابن الماء وإذا وضع فيه مات، فما هو؟", "c": ["الثلج", "السمك", "الملح"], "a": "الثلج"},
    {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "c": ["القلم", "الكتاب", "الدفتر"], "a": "القلم"},
    {"q": "ما هو الشيء الذي له عين واحدة ولا يرى؟", "c": ["الإبرة", "الكاميرا", "الباب"], "a": "الإبرة"},
    {"q": "ما هو الباب الذي لا يمكن فتحه؟", "c": ["الباب المفتوح", "باب الخيال", "الباب المغلق"], "a": "الباب المفتوح"},
    {"q": "أخت خالك وليست خالتك، من تكون؟", "c": ["أمك", "جدتك", "عمتك"], "a": "أمك"},
    {"q": "ما هو الشيء الذي قلبه يأكل قشره؟", "c": ["الشمعة المشتعلة", "البطيخ", "التفاح"], "a": "الشمعة المشتعلة"},
    {"q": "من هو الشخص الذي يرى صديقه وعدوه بعين واحدة؟", "c": ["الأعور", "الأعمى", "الحكيم"], "a": "الأعور"},
    {"q": "شيء موجود في السماء إذا أضفت إليه حرفاً أصبح في الأرض؟", "c": ["نجم", "غيم", "قمر"], "a": "نجم"},
    {"q": "له أوراق وما هو بنبات، وله جلد وما هو بحيوان؟", "c": ["الكتاب", "الشجر", "الخيمة"], "a": "الكتاب"},
    {"q": "ما هو الشيء الذي إذا غليته جمد؟", "c": ["البيض", "الماء", "الحليب"], "a": "البيض"},
    {"q": "ما هو الشيء الذي يجتاز الزجاج ولا يكسره؟", "c": ["الضوء", "الصوت", "الماء"], "a": "الضوء"},
    {"q": "كله ثقوب ومع ذلك يحفظ الماء؟", "c": ["الإسفنج", "المصفاة", "الشبكة"], "a": "الإسفنج"},
    {"q": "ما هو الشيء الذي لا يمشي إلا بالضرب؟", "c": ["المسمار", "الكرة", "الطبل"], "a": "المسمار"},
    {"q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟", "c": ["التليفون", "الراديو", "التلفاز"], "a": "التليفون"},
    {"q": "يتحرك دائماً ولا يراه أحد، فما هو؟", "c": ["الهواء", "الزمن", "الظل"], "a": "الهواء"},
    {"q": "طائر يلد ولا يبيض، ما هو؟", "c": ["الوطواط", "النعامة", "البطريق"], "a": "الوطواط"},
    {"q": "ما هو الشيء الذي تذبحه وتبكي عليه؟", "c": ["البصل", "الدجاج", "الخروف"], "a": "البصل"},
    {"q": "ما هو الشيء الذي ترميه كلما احتجت إليه؟", "c": ["شبكة الصيد", "القمامة", "الكرة"], "a": "شبكة الصيد"},
    {"q": "مدينة سعودية تقرأ طردياً وعكسياً بنفس اللفظ؟", "c": ["العلا", "الدمام", "جدة"], "a": "العلا"},
    {"q": "ما هو الشيء الذي لك ولكن أصدقاؤك يستخدمونه أكثر منك؟", "c": ["اسمك", "رقمك", "بيتك"], "a": "اسمك"},
    {"q": "عقرب لا يلدغ ولا يخاف منه أحد؟", "c": ["عقرب الساعة", "عقرب ميت", "عقرب لعبة"], "a": "عقرب الساعة"},
    {"q": "ما هو الشيء الذي نرميه بعد العصر؟", "c": ["البرتقال", "التفاح", "العنب"], "a": "البرتقال"}
]

active_riddles = {}

@Client.on_message(filters.text & filters.group, group=80)
def riddle_message_handler(c, m):
    if not getattr(m, 'from_user', None):
        return
    
    # التحقق من أن البوت مفعل في المجموعة
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return
        
    # التحقق من أن الألعاب غير معطلة
    if r.get(f'{m.chat.id}:disableGames:{Dev_Zaid}'):
        return
    
    text = m.text.strip()
    
    # التحقق من اسم البوت في حالة النداء
    bot_name = r.get(f'{Dev_Zaid}:BotName') or 'رعد'
    if text.startswith(f'{bot_name} '):
        text = text.replace(f'{bot_name} ', '')
        
    if text == "لغز":
        riddle = random.choice(riddles_data)
        choices = riddle["c"].copy()
        random.shuffle(choices)
        
        # إنشاء معرف فريد للعبة
        game_id = f"r_{m.chat.id}_{int(time.time())}_{random.randint(100, 999)}"
        
        keyboard = []
        for choice in choices:
            is_correct = 1 if choice == riddle["a"] else 0
            keyboard.append([InlineKeyboardButton(choice, callback_data=f"rdl:{game_id}:{is_correct}")])
            
        markup = InlineKeyboardMarkup(keyboard)
        msg = m.reply(riddle["q"], reply_markup=markup)
        
        # حفظ بيانات اللعبة النشطة
        active_riddles[game_id] = {
            "q": riddle["q"],
            "a": riddle["a"],
            "msg_id": msg.id,
            "chat_id": m.chat.id
        }
        
        # تعيين مؤقت لإنهاء اللغز إذا لم يتم الإجابة عليه
        Thread(target=_expire_riddle, args=(game_id, 60), daemon=True).start()

def _expire_riddle(game_id, seconds):
    time.sleep(seconds)
    if game_id in active_riddles:
        del active_riddles[game_id]

@Client.on_callback_query(filters.regex(r'^rdl:'))
def riddle_callback_handler(c, m):
    if not getattr(m, 'from_user', None):
        return
    
    data = m.data
    parts = data.split(":")
    if len(parts) < 3:
        return m.answer("❌ خطأ", show_alert=False)
    
    game_id = parts[1]
    is_correct = parts[2] == "1"
    
    if game_id not in active_riddles:
        return m.answer("⏰ انتهى الوقت أو تم الإجابة على هذا اللغز!", show_alert=True)
    
    game = active_riddles[game_id]
    correct_ans = game["a"]
    
    if is_correct:
        # إعطاء مكافأة للفائز
        reward = random.randint(10, 50)
        user_id = m.from_user.id
        if r.get(f'{user_id}:Floos'):
            floos = int(r.get(f'{user_id}:Floos'))
            r.set(f'{user_id}:Floos', floos + reward)
        else:
            r.set(f'{user_id}:Floos', reward)
            
        m.answer("✅ إجابة صحيحة!", show_alert=False)
        m.edit_message_text(
            f"✅ الفائز: {m.from_user.mention}\n"
            f"🎯 الإجابة: {correct_ans}\n"
            f"💸 الجائزة: {reward} ريال",
            disable_web_page_preview=True
        )
        # حذف اللغز من النشطة حتى لا يجيب عليه شخص آخر
        del active_riddles[game_id]
    else:
        m.answer("❌ إجابة خاطئة! جرب مرة أخرى", show_alert=True)
