# handlers/users/main/menu.py



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.reply_filters import (
    MyFriendsFilter,
    StatisticsFilter,
    GameRulesFilter,
    ReferralLinkFilter,
    MyGiftsFilter,
    ContactAdminFilter
)
from data.constants import REFERRAL_MESSAGE, REFERRAL_REPLY, PHOTO_URL
from keyboards.default import main_keyboard
from middlewares.checksub import success_text, photo
from utils.database import db

router = Router()


@router.message(MyFriendsFilter())
async def show_my_friends(message: Message):
    try:
        # Foydalanuvchi ID sini olamiz
        user_id = message.from_user.id

        # Botdan referal linki
        bot_username = (await message.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={user_id}"

        # Foydalanuvchining referallari sonini olamiz
        user_data = await db.get_user(user_id)
        ref_count = user_data.get('ref_count', 0) if user_data else 0

        # Statistika xabarini yuboramiz
        text = (
            f"📊 Sizning statistikangiz\n\n"
            f"Sizning ID: {user_id}\n"
            f"Siz to'plagan ballar: {ref_count} ball\n\n"
            f"(⭐️ Do'stingiz barcha shartlarni bajarsa sizga ballar yoziladi)"
        )

        # Do'stlarga ulashish tugmasi
        share_button = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="↗️ Do'stlarga ulashish",
                url=f"https://t.me/share/url?url={referal_link}"
            )
        ]])

        await message.answer(text, reply_markup=share_button)

    except Exception as e:
        print(f"Error in show_my_friends: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")




@router.message(StatisticsFilter())
async def show_statistics(message: Message):
    try:
        # Foydalanuvchi referallarini olamiz
        user_id = message.from_user.id

        # Bot username va referal linkni yaratamiz
        bot_username = (await message.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={user_id}"

        # Bazadan ma'lumotlarni olamiz
        ref_count = await db.get_user_referrals_count(user_id)

        text = (
            f"✅ Sizning shartlarni bajargan do'stlaringiz: {ref_count} ta\n"
            f"🎯 Do'stlaringizni botga taklif qiling!"
        )

        # Do'stlarga ulashish tugmasi
        share_button = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="↗️ Do'stlarga ulashish",
                    url=f"https://t.me/share/url?url={referal_link}"
                )
            ]]
        )

        await message.answer(text, reply_markup=share_button)

    except Exception as e:
        print(f"Error in show_statistics: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")



@router.message(GameRulesFilter())
async def show_game_rules(message: Message):
    try:
        # O'yin shartlari matni
        rules_text = (
            "Sovg'alar ro'yxati bilan tanishtiraman:\n\n"
            "🥇Eng ko'p odam qo'shgan ishtirokchi: Hilola Yussupova bilan 1 kun. (Bu kun biznes zavtrak, obed va shopping Hilola Yussupova tomonidan qilib beriladi)\n\n"
            "🏆 10 ta obunachi: \"Hayotni sev\" maqsadlar workbook qo'llanmasi\n"
            "🏆 20 ta obunachi: \"Hayotni sev\" maqsadlar workbook qo'llanmasi va \"Hayotni sev\" 2 ta darsligi\n"
            "🏆 50 ta obunachi: \"Hayotni sev\" premium ta'rifi+ \"Hayotni sev\" maqsadlar workbook qo'llanmasi\n"
            "🏆 100 ta obunachi: \"O'zim\" kursi premium ta'rifi +\"Hayotni sev\" workbook qo'llanmasi + \"Hayotni sev\" premium ta'rifi.\n"
            "🏆 500 ta obunachi: Yuqoridagi barcha kurslar + Hilola Yussupovadan konsultatsiya\n"
            "🏆 1,000 ta obunachi: Hilola Yusupova bilan bizness nonushta\n\n"
            "🎁 G'olib 6-oktabr kuni vebinar vaqti aniqlanadi\n"
            "🧮 Yaqinlaringizni taklif qilganingizni mana shu bot hisoblab boradi, Har bir siz tomondan qo'shilgan odam haqida xabar yuboradi.\n"
            "🎁 Qo'shgan odamlaringiz soni ko'paygani sari sovg'alar egasi bo'lish imkoningiz ham oshadi.\n\n"
            "Siz uchun maxsus linki beriladi! Uni faqat siz ishlata olasiz 🫶🏼\n"
            f"👉 @HilolaYussupovabot (https://t.me/HilolaYussupovabot?start={message.from_user.id})\n"
            "📌Ushbu linkni tanishlaringizga yuboring!\n"
            "Har bir qo'shgan insoningiz sizga 1 ball olib keladi!\n\n"
            "(Diqqat ushbu o'yin faqat ayol va qizlar uchun. Erkaklar qatnasha olishmaydi ❌)"
        )

        start_game_button = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🎮 O'yinni boshlash", callback_data="start_game")
            ]]
        )

        await message.answer(rules_text, reply_markup=start_game_button)

    except Exception as e:
        print(f"Error in game rules: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

@router.callback_query(F.data == "start_game")
async def start_game(callback: CallbackQuery):
    try:
        # Referral linkni yaratish
        bot_username = (await callback.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={callback.from_user.id}"

        # Avvalgi xabarni o'chiramiz
        await callback.message.delete()

        # Rasimli xabar yuborish
        msg = await callback.message.answer_photo(
            photo=PHOTO_URL,
            caption=REFERRAL_MESSAGE.format(referal_link=referal_link),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="🎁 Sovg'ani olish", callback_data="get_gift")
                ]]
            )
        )

        # Reply xabar
        await msg.reply(REFERRAL_REPLY)
        await callback.answer()

    except Exception as e:
        print(f"Error in start game: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "get_gift")
async def get_gift(callback: CallbackQuery):
    try:
        # Avvalgi xabarni o'chiramiz
        await callback.message.delete()

        # Sovg'ani olish xabari
        await callback.message.answer_photo(
            photo=photo,
            caption=success_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="Ha, xohlayman!", callback_data="confirm_participation")
                ]]
            )
        )
        await callback.answer()

    except Exception as e:
        print(f"Error in get gift: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)




@router.message(ReferralLinkFilter())
async def get_referral_link(message: Message):
    try:
        # Referal linkni yaratamiz
        bot_username = (await message.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={message.from_user.id}"

        # Rasimli xabar yuborish
        msg = await message.answer_photo(

            photo="https://github.com/JasurShermatov/logo/blob/main/photo_2024-12-07_12-12-33.jpg?raw=true",  # O'zingizning rasm URL/path
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

        # Reply xabar
        await msg.reply(
            "ℹ️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!\n"
            "Uni do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating!"
        )

    except Exception as e:
        print(f"Error in referral: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")


@router.message(MyGiftsFilter())
async def show_my_gifts(message: Message):
    try:
        # Referal linkni yaratish
        bot_username = (await message.bot.me()).username
        referal_link = f"https://t.me/{bot_username}?start={message.from_user.id}"

        # Sovg'alar text
        gifts_text = (
            "Sizda hali sovg'alar mavjud emas!\n\n"
            "Sovg'alarni yutib olishingiz uchun ko'proq do'stingizni taklif qiling!"
        )

        # Share button
        share_button = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="↗️ Do'stlarga ulashish",
                    url=f"https://t.me/share/url?url={referal_link}"
                )
            ]]
        )

        await message.answer(gifts_text, reply_markup=share_button)

    except Exception as e:
        print(f"Error in show my gifts: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")




@router.message(ContactAdminFilter())
async def contact_admin(message: Message):
   try:
       # Admin bilan bog'lanish matni
       admin_text = (
           "🥰 Agar sizda ushbu bot bo'yicha savollar yoki qo'shimcha "
           "ma'lumot olish istagi bo'lsa, murojaat qiling!\n\n"
           "Bizga savol yo'llang, biz sizning savollaringiz va "
           "qiziqishlaringizga tezkor javob berishga tayyormiz! 🎯"
       )

       # Orqaga qaytish tugmasi
       back_button = ReplyKeyboardMarkup(
           keyboard=[[
               KeyboardButton(text="⬅️ Orqaga")
           ]],
           resize_keyboard=True
       )

       await message.answer(admin_text, reply_markup=back_button)

   except Exception as e:
       print(f"Error in contact admin: {e}")
       await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

# Orqaga tugmasi uchun handler
@router.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: Message):
   try:
       await message.answer(
           "Asosiy menyuga qaytdingiz",
           reply_markup=main_keyboard
       )
   except Exception as e:
       print(f"Error in back to main: {e}")
       await message.answer("❌ Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")