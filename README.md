# 🤖 Telegram Bot (Pyrogram + Redis)

بوت تيليجرام متعدد الوظائف مبني بـ **Pyrogram** مع **Redis** للتخزين المؤقت و **SQLite** لقواعد البيانات.

---

## ✨ المميزات

- 🎮 ألعاب (XO, Akinator, وغيرها)
- 🎵 تحميل الصوتيات والفيديوهات (YouTube, وغيرها)
- 👥 إدارة المجموعات (رتب، حظر، كتم)
- 🛡️ فلاتر وأوامر مخصصة
- 🎉 ترحيب وقوانين
- 📖 القرآن الكريم
- 🔒 نظام صلاحيات متعدد المستويات
- 💬 الوسوسة (Whisper)

---

## 📋 المتطلبات

- **Python** 3.10+
- **Redis** Server
- **FFmpeg** (للوسائط)
- **Telegram Bot Token** (من [@BotFather](https://t.me/BotFather))

---

## 🚀 التثبيت المحلي

### 1. استنساخ المشروع
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. إعداد المتغيرات البيئية
```bash
cp .env.example .env
```
ثم عدّل ملف `.env` وأضف بياناتك:
```env
BOT_TOKEN=توكن_البوت_هنا
SUDO_ID=آيدي_المطور
BOT_USERNAME=يوزر_البوت
REDIS_URL=redis://localhost:6379
```

### 3. التثبيت السريع (Linux)
```bash
bash start.sh
```

### 3. التثبيت اليدوي
```bash
# تثبيت FFmpeg و Redis
sudo apt-get install -y ffmpeg redis-server
sudo service redis-server start

# تثبيت مكتبات Python
pip install -r requirements.txt

# تشغيل البوت
python main.py
```

---

## ☁️ النشر على Render

### 1. إنشاء خدمة Redis
- اذهب إلى [Render Dashboard](https://dashboard.render.com)
- أنشئ **New Redis** وانسخ رابط الاتصال (`Internal URL`)

### 2. إنشاء خدمة Worker
- اذهب إلى **New > Background Worker**
- اربط مستودع GitHub
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  python main.py
  ```

### 3. إعداد المتغيرات البيئية
في قسم **Environment** أضف:

| المتغير | الوصف |
|---------|-------|
| `BOT_TOKEN` | توكن البوت من BotFather |
| `SUDO_ID` | آيدي حساب المطور |
| `BOT_USERNAME` | يوزرنيم البوت |
| `REDIS_URL` | رابط Redis الداخلي من Render |

### 4. النشر التلقائي
كل `push` على GitHub سيُعاد نشر البوت تلقائياً على Render.

---

## 📁 هيكل المشروع

```
├── main.py              # نقطة الدخول الرئيسية
├── config.py            # الإعدادات والاتصالات
├── requirements.txt     # مكتبات Python
├── Procfile             # إعدادات Render
├── render.yaml          # Blueprint لـ Render
├── start.sh             # سكربت التثبيت السريع
├── .env.example         # نموذج المتغيرات البيئية
├── .gitignore           # الملفات المستثناة من Git
├── source_image.jpg     # صورة البوت
├── Plugins/             # إضافات البوت
│   ├── all.py           # الأوامر العامة
│   ├── clean.py         # التنظيف التلقائي
│   ├── games.py         # الألعاب
│   ├── downloader.py    # التحميل
│   ├── fun.py           # المرح
│   ├── set_ranks.py     # إعداد الرتب
│   └── ...              # وغيرها
├── helpers/             # دوال مساعدة
│   ├── Ranks.py         # نظام الرتب
│   ├── games.py         # منطق الألعاب
│   ├── memes.py         # الميمز
│   └── ...              # وغيرها
├── scripts/             # سكربتات صيانة
│   └── ...
└── downloads/           # مجلد التحميلات (مؤقت)
```

---

## ⚠️ ملاحظات مهمة

- **لا ترفع ملف `.env`** على GitHub — يحتوي أسراراً!
- **ملفات Session** (`.session`) تُنشأ تلقائياً ومحمية بـ `.gitignore`
- **قواعد البيانات** (`*.sqlite`) تُنشأ تلقائياً عند التشغيل
- **مجلد `downloads/`** يُستخدم مؤقتاً للتحميلات ومحمي بـ `.gitignore`

---

## 📝 الترخيص

هذا المشروع للاستخدام الخاص.
