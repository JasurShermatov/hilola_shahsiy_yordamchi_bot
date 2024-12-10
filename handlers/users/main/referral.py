# handlers/users/main/referral.py
from aiogram import Router, F
from aiogram.types import Message
from utils.database import db  # Importni to'g'irlandi

router = Router()


@router.message(F.text == "👥 DO'STLARIM")
async def show_referrals(message: Message):
    user_id = message.from_user.id

    # Referal ma'lumotlarini olish
    ref_data = await db.get_user_referrals(user_id)

    # Xabar matni
    text = [
        "👥 Sizning do'stlaringiz:",
        f"✅ Jami do'stlar soni: {ref_data['total_count']} ta",
        f"🆕 So'nggi 24 soatda: {ref_data['last_day_count']} ta\n",
    ]

    # Referallar ro'yxati
    if ref_data["referrals"]:
        text.append("Do'stlaringiz ro'yxati:")
        for i, ref in enumerate(ref_data["referrals"], 1):
            username = ref["username"] if ref["username"] else ref["full_name"]
            date = ref["created_at"].strftime("%Y-%m-%d %H:%M")
            text.append(f"{i}. {username} - {date}")
    else:
        text.append("\nHozircha do'stlaringiz yo'q. Do'stlaringizni taklif qiling!")

    await message.answer("\n".join(text))
