# data/constants.py

# Start komandasi uchun xabar
START_TEXT = (
    "Just_adam, tabriklaymiz!\n"
    "Siz «Hilola Yusupova» ning \"O'zim\" onlayn vebinariga muvaffaqiyatli ro'yxatdan o'tdingiz ✅\n\n"
    "⏰ 6-OKTABR SOAT 20:20 da o'zingizni to'liq agnlash va yaxshilashni to'liq o'rganib olasiz ✨\n\n"
    "Va bu ma'lumotlar hayotingizni tubdan o'zgartirib yuborishi mumkin 🥰\n\n"
    "🎁 Ushbu botda esa do'stlaringizni botga taklif qilish orqali bir nechta kurslarimga, "
    "bundan tashqari mendan konsultatsiya va bir nechta sovg'alarga ega bo'lasiz 🚀\n\n"
    "Hoziroq vebinar bo'ladigan kanalga qo'shiling, buning uchun «KANALGA O'TISH» tugmasini bosing\n"
    "👇🏻👇🏻👇🏻"
)
PHOTO_URL2="https://github.com/JasurShermatov/logo/blob/main/photo_2024-12-08_17-07-28.jpg?raw=true"


# Obuna tekshirilganda chiqadigan xabar
SUBSCRIPTION_SUCCESS = "Tabriklaymiz! Siz muvaffaqiyatli obuna bo'ldingiz!"

# Referal xabari
REFERRAL_MESSAGE = (
    "🎁 Do'stim!!! Sizga sovg'am bor 👇\n\n"
    "💕 Hilola Yussupova o'z obunachilariga bepul darslar va sovg'alar tarqatyabdi\n\n"
    "✅ Buning uchun quyidagi botga kirib shartlarni bajaring va hoziroq yopiq kanalga ulaning:\n\n"
    "👉 {referal_link}"
)

# Reply xabar
REFERRAL_REPLY = (
    "⬆️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!\n\n"
    "Uni do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating "
    "hamda o'z sovg'angizni qo'lga kiriting! Omad🔥"
)

# Rasm URL
PHOTO_URL = "https://telegra.ph/file/a72f5f1ae304aefa9c606.jpg"

# Tugmalar matni
BUTTONS = {
    'SUBSCRIBE': "✅ OBUNA BO'LISH",
    'CHECK': "♻️ TEKSHIRISH",
    'CONFIRM': "Ha, xohlayman!",
    'GET_GIFT': "🎁 Sovg'ani olish"
}

# Admin panel xabarlari
ADMIN_MESSAGES = {
    'WELCOME': """
🔐 Admin panel

«Hilola Yusupova» botining admin paneliga xush kelibsiz!
Quyidagi bo'limlardan birini tanlang:""",

    'STATS': """
📊 Bot statistikasi:

👥 Jami foydalanuvchilar: {total_users} ta
📅 Bugun qo'shilganlar: {today_users} ta
👨‍👩‍👧‍👦 Do'stlarini taklif qilganlar: {active_refs} ta

💫 Oxirgi 24 soat:
├─ Yangi a'zolar: {new_today} ta
└─ Faol referallar: {new_refs} ta""",

    'EXPORT_STARTED': "📤 Excel fayl tayyorlanmoqda...",

    'EXPORT_READY': """
📊 Foydalanuvchilar ro'yxati:

Ushbu faylda quyidagi ma'lumotlar mavjud:
- Foydalanuvchi ID raqami
- Username
- To'liq ismi
- Ro'yxatdan o'tgan sanasi
- Taklif qilgan do'stlari soni
- Aktivlik holati""",

    'BROADCAST_START': """
📢 Xabar yuborish

Iltimos, tarqatmoqchi bo'lgan xabar matnini kiriting.
Bekor qilish uchun /cancel buyrug'ini yuboring.""",

    'BROADCAST_PROGRESS': "📨 Xabar yuborilmoqda...\n\nYuborildi: {sent}/{total}",

    'BROADCAST_COMPLETE': "✅ Xabar yuborish yakunlandi\n\nYuborildi: {sent}/{total}"
}