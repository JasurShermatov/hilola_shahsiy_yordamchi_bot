# keyboards/default/main_kb.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👥 DO'STLARIM"), KeyboardButton(text="📊 STATISTIKA")],
        [
            KeyboardButton(text="🏆 O'YIN SHARTLARI"),
            KeyboardButton(text="♻️ REFERAL LINKNI OLISH"),
        ],
        [
            KeyboardButton(text="🎁 MENING SOVG'ALARIM"),
            KeyboardButton(text="💭 ADMIN BILAN BOG'LANISH"),
        ],
    ],
    resize_keyboard=True,
)
