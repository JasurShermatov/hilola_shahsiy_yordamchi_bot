from aiogram import Router, F
from aiogram.types import FSInputFile
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.filters import Command, CommandStart

from data.config import load_config
from keyboards.default.main_kb import main_keyboard
from keyboards.inline.channel_kb import channel_keyboard, confirmation_keyboard
from data.constants import (
    START_TEXT,
    PHOTO_URL2,
    SUBSCRIPTION_SUCCESS,
    REFERRAL_MESSAGE,
    REFERRAL_REPLY,
    PHOTO_URL,
    BUTTONS,
)
from utils.database.functions.users import Database

config = load_config()
db = Database()
router = Router()


@router.message(CommandStart())
async def start_command(message: Message, command: CommandStart):
    try:
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        username = message.from_user.username or str(message.from_user.id)

        referrer_id = command.args if command.args and command.args.isdigit() else None

        await db.create_pool(config=config)

        await db.add_user(
            user_id=message.from_user.id,
            username=username,
            full_name=full_name,
            referrer_id=referrer_id,
        )

        print(f"User created: {full_name}, referred by: {referrer_id}")

        await message.answer_photo(
            photo=PHOTO_URL2, caption=START_TEXT, reply_markup=channel_keyboard
        )

    except Exception as e:
        print(f"Error in start command: {e}")
        await message.answer_photo(
            photo=PHOTO_URL2, caption=START_TEXT, reply_markup=channel_keyboard
        )


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    try:
        await callback.message.delete()

        await callback.message.answer(
            "Botimizning asosiy menyusiga xush kelibsiz!", reply_markup=main_keyboard
        )

        await callback.message.answer(
            text=SUBSCRIPTION_SUCCESS, reply_markup=confirmation_keyboard
        )

    except Exception as e:
        print(f"Error in check subscription: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "confirm_participation")
async def confirm_participation(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        bot_username = (await callback.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={user_id}"

        await callback.message.delete()

        await callback.message.answer(
            "Botimizning asosiy menyusiga xush kelibsiz!", reply_markup=main_keyboard
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
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🎁 Sovg'ani olish", callback_data="get_gift"
                        )
                    ]
                ]
            ),
        )

        # Reply xabar yuborish
        await msg.reply(
            "ℹ️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!\n"
            "Uni do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating!"
        )

    except Exception as e:
        print(f"Error in confirmation: {e}")
        await callback.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")
