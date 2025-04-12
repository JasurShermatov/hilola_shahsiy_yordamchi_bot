# keyboards/inline/channel_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import load_config

config = load_config()

channel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ OBUNA BO'LISH",
                url=config.bot.channel_url,  # .bot qo'shildi
            )
        ],
        [InlineKeyboardButton(text="♻️ TEKSHIRISH", callback_data="check_subscription")],
    ]
)

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Ha, xohlayman!", callback_data="confirm_participation"
            )
        ]
    ]
)
