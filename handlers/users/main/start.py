# handlers/users/main/start.py
from aiogram import Router, F
from aiogram.types import FSInputFile
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.filters import Command, CommandStart
from keyboards.default.main_kb import main_keyboard
from keyboards.inline.channel_kb import channel_keyboard, confirmation_keyboard
from data.constants import (
    START_TEXT,
    PHOTO_URL2,
    SUBSCRIPTION_SUCCESS,
    REFERRAL_MESSAGE,
    REFERRAL_REPLY,
    PHOTO_URL,
    BUTTONS
)
from utils.database.db_init import create_user

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    try:
        # Safely combine first_name and last_name
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()

        # If username is None, use string representation of user_id
        username = message.from_user.username or str(message.from_user.id)

        await create_user(
            user_id=message.from_user.id,
            username=username,
            full_name=full_name,
            referrer_id="12345"
        )
        print(f"User created: {full_name}")

        await message.answer_photo(
            photo=PHOTO_URL2,
            caption=START_TEXT,
            reply_markup=channel_keyboard
        )

    except Exception as e:
        print(f"Error in start command: {e}")
        # Send start message even if there's an error
        await message.answer_photo(
            photo=PHOTO_URL2,
            caption=START_TEXT,
            reply_markup=channel_keyboard
        )

@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    try:
        # Avval eski xabarni o'chiramiz
        await callback.message.delete()

        # Asosiy menu chiqaramiz
        await callback.message.answer(
            "Botimizning asosiy menyusiga xush kelibsiz!",
            reply_markup=main_keyboard
        )

        # Success xabarni yuboramiz
        await callback.message.answer(
            text=SUBSCRIPTION_SUCCESS,
            reply_markup=confirmation_keyboard
        )

    except Exception as e:
        print(f"Error in check subscription: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)



@router.callback_query(F.data == "confirm_participation")
async def confirm_participation(callback: CallbackQuery):
    try:
        # Referral linkni yaratish
        user_id = callback.from_user.id
        bot_username = (await callback.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={user_id}"

        # Avvalgi xabarni o'chiramiz
        await callback.message.delete()

        # Main menu ni yuboramiz
        await callback.message.answer(
            "Botimizning asosiy menyusiga xush kelibsiz!",
            reply_markup=main_keyboard  # Asosiy menu tugmalari
        )

        # Rasimli xabar yuborish
        photo = "https://github.com/JasurShermatov/logo/blob/main/photo_2024-12-07_12-21-44.jpg?raw=true"
        msg = await callback.message.answer_photo(
            photo=photo,
            caption=(
                f"🎁 Do'stim!!!! Sizga sovg'am bor ⚡️\n\n"
                f"💝 Hilola Yussupova o'z o'bunachilariga bepul darslar va sovg'alar tarqatyabdi\n\n"
                f"✅ Buning uchun quyidagi botga kirib shartlarni bajaring va hoziroq yopiq kanalga ulaning:\n\n"
                f"👉 {referal_link}\n\n"
                f"ℹ️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!\n\n"
                f"Uni do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating hamda o'z sovg'angizni qo'lga kiriting! Omad! 🔥"
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="🎁 Sovg'ani olish", callback_data="get_gift")
                ]]
            )
        )

        # Reply xabar yuborish
        await msg.reply(
            "ℹ️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!\n"
            "Uni do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating!"
        )

    except Exception as e:
        print(f"Error in confirmation: {e}")
        await callback.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")