# middlewares/checksub.py
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from data.config import load_config
from keyboards.default.main_kb import main_keyboard

success_text = (
    "🏆 Assalomu alaykum xush kelibsiz!\n\n"
    "😊 Sizga ajoyib imkoniyatlarni taqdim etmoqchiman: bepul kurslar "
    "va shaxsiy konsultatsiyalarga ega bo'lishingiz mumkin! 🎁\n\n"
    "🎯 Sovg'ani olish shartlari juda oddiy:\n"
    "Do'stlaringiz va yaqinlaringizni ushbu bot va kanalimizga "
    "qo'shing.\n"
    "Kim ko'p do'stlarini qo'shsa, eng zo'r sovg'alarni qo'lga kiritadi!\n\n"
    "📚 Bonus: Kanalimizda BEPUL DARSLIKLAR mavjud! O'zingizni "
    "rivojlantirishga shoshiling va yaqinlaringizga ham tavsiya "
    "qiling! 🌟\n\n"
    "🎁 Sovg'alar olish uchun:\n"
    'Botimizga va "O\'zim" onlayn vebinariga dugonangiz yoki '
    "tanishlaringizni qo'shing va maxsus sovg'alar yutib oling!"
)

photo = "https://github.com/JasurShermatov/logo/blob/main/photo_2024-12-07_12-21-44.jpg?raw=true"


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def check_subscription(self, user_id: int, bot) -> bool:
        try:
            channel_username = load_config().bot.channel_id
            member = await bot.get_chat_member(
                chat_id=channel_username, user_id=user_id
            )
            return member.status in ["member", "administrator", "creator"]
        except Exception as e:
            print(f"Error checking subscription: {e}")
            return False

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        bot = data["bot"]

        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            is_subscribed = await self.check_subscription(user_id, bot)
            if not is_subscribed:
                await event.answer(
                    "Iltimos, avval kanalga obuna bo'ling!", show_alert=True
                )
                return

            # Asosiy menu va tugmalarni yuboramiz
            await event.message.answer(
                "Botimizning asosiy menyusiga xush kelibsiz!",
                reply_markup=main_keyboard,
            )

            try:
                # Eski xabarni o'chiramiz
                await event.message.delete()

                # Yangi xabarni rasm bilan yuboramiz
                await event.message.answer_photo(
                    photo=photo,
                    caption=success_text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Ha, xohlayman!",
                                    callback_data="confirm_participation",
                                )
                            ]
                        ]
                    ),
                )
            except Exception as e:
                print(f"Error updating message: {e}")
                await event.message.answer(
                    text=success_text,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Ha, xohlayman!",
                                    callback_data="confirm_participation",
                                )
                            ]
                        ]
                    ),
                )
            return

        if isinstance(event, Message):
            is_subscribed = await self.check_subscription(user_id, bot)
            if not is_subscribed:
                return await handler(event, data)

        return await handler(event, data)
