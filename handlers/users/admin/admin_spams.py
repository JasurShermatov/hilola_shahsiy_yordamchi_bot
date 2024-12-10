# handlers/users/admin/admin_spams.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data.config import load_config
from utils.database import db

router = Router()


# Admin filterini yaratamiz
def is_admin(user_id: int) -> bool:
    return user_id in load_config().bot.admin_ids


class BroadcastStates(StatesGroup):
    waiting_message = State()


@router.message(Command("broadcast"), lambda msg: is_admin(msg.from_user.id))
async def start_broadcast(message: Message, state: FSMContext):
    await message.answer("Iltimos, tarqatmoqchi bo'lgan xabarni yuboring.")
    await state.set_state(BroadcastStates.waiting_message)


@router.message(BroadcastStates.waiting_message)
async def process_broadcast(message: Message, state: FSMContext):
    users = await db.get_all_users()
    count = 0
    errors = 0

    await message.answer("Xabar yuborish boshlandi...")

    for user in users:
        try:
            await message.copy_to(user['user_id'])
            count += 1
        except Exception as e:
            errors += 1
            print(f"Error sending message to {user['user_id']}: {e}")

        # Har 10 ta xabardan keyin progress xabar
        if count % 10 == 0:
            await message.answer(f"Yuborildi: {count} ta\nXato: {errors} ta")

    await message.answer(
        f"Xabar yuborish yakunlandi.\n"
        f"Yuborildi: {count} ta\n"
        f"Xato: {errors} ta"
    )
    await state.clear()