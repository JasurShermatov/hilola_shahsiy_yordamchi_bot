# handlers/users/admin/admin.py
import pandas as pd
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from data.config import load_config
from filters.admin import AdminFilter
from keyboards.default.admin_kb import admin_keyboard
from keyboards.default.main_kb import main_keyboard
from utils.database import db

router = Router()

# Admin ID larni yuklab olish
ADMIN_IDS = load_config().bot.admin_ids


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Bu buyruq faqat adminlar uchun!")
        return

    await message.answer(
        "👋 Admin panel:\n\n"
        "🔍 Quyidagi funksiyalardan foydalanishingiz mumkin:",
        reply_markup=admin_keyboard
    )


@router.message(F.text == "📊 Statistika", AdminFilter())
async def show_statistics(message: Message):
    try:
        # Asosiy statistikalar
        total_users = await db.get_users_count()
        today_users = await db.get_today_users_count()
        active_refs = await db.get_active_referrers_count()

        # Top referallar
        top_refs = await db.get_top_referrers(limit=10)

        # Haftalik statistika
        weekly_stats = await db.get_weekly_stats()

        # Statistika matni
        stats = [
            "📊 Bot statistikasi\n",
            f"👥 Jami foydalanuvchilar: {total_users:,} ta",
            f"📅 Bugun qo'shilganlar: {today_users} ta",
            f"♻️ Referal berganlar: {active_refs} ta\n"
        ]

        # Top referallar qo'shish
        if top_refs:
            stats.append("🏆 TOP-10 Faol referallar:")
            for i, user in enumerate(top_refs, 1):
                username = f"@{user['username']}" if user['username'] else user['full_name']
                stats.append(f"{i}. {username}: {user['ref_count']} ta taklif")
            stats.append("")

        # Haftalik statistika qo'shish
        if weekly_stats:
            stats.append("📈 So'nggi 7 kunlik statistika:")
            for date, count in weekly_stats.items():
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
                stats.append(f"📅 {formatted_date}: +{count} ta")

        await message.answer("\n".join(stats))

    except Exception as e:
        print(f"Error showing statistics: {e}")
        await message.answer("❌ Statistikani olishda xatolik yuz berdi")

# handlers/users/admin/admin.py
import pandas as pd
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from data.config import load_config
from filters.admin import AdminFilter
from keyboards.default.admin_kb import admin_keyboard
from keyboards.default.main_kb import main_keyboard
from utils.database import db

router = Router()

# Admin ID larni yuklab olish
ADMIN_IDS = load_config().bot.admin_ids


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Bu buyruq faqat adminlar uchun!")
        return

    await message.answer(
        "👋 Admin panel:\n\n"
        "🔍 Quyidagi funksiyalardan foydalanishingiz mumkin:",
        reply_markup=admin_keyboard
    )


@router.message(F.text == "📊 Statistika", AdminFilter())
async def show_statistics(message: Message):
    try:
        # Asosiy statistikalar
        total_users = await db.get_users_count()
        today_users = await db.get_today_users_count()
        active_refs = await db.get_active_referrers_count()

        # Top referallar
        top_refs = await db.get_top_referrers(limit=10)

        # Haftalik statistika
        weekly_stats = await db.get_weekly_stats()

        # Statistika matni
        stats = [
            "📊 Bot statistikasi\n",
            f"👥 Jami foydalanuvchilar: {total_users:,} ta",
            f"📅 Bugun qo'shilganlar: {today_users} ta",
            f"♻️ Referal berganlar: {active_refs} ta\n"
        ]

        # Top referallar qo'shish
        if top_refs:
            stats.append("🏆 TOP-10 Faol referallar:")
            for i, user in enumerate(top_refs, 1):
                username = f"@{user['username']}" if user['username'] else user['full_name']
                stats.append(f"{i}. {username}: {user['ref_count']} ta taklif")
            stats.append("")

        # Haftalik statistika qo'shish
        if weekly_stats:
            stats.append("📈 So'nggi 7 kunlik statistika:")
            for date, count in weekly_stats.items():
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
                stats.append(f"📅 {formatted_date}: +{count} ta")

        await message.answer("\n".join(stats))

    except Exception as e:
        print(f"Error showing statistics: {e}")
        await message.answer("❌ Statistikani olishda xatolik yuz berdi")


@router.message(F.text == "📥 Users Excel", AdminFilter())
async def get_users_excel(message: Message):
    await message.answer("📊 Excel fayl tayyorlanmoqda...")

    try:
        users = await db.get_all_users()

        if not users:
            await message.answer("❌ Foydalanuvchilar topilmadi")
            return

        # DataFrame yaratish
        df = pd.DataFrame(users)

        # Ustunlarni formatlash
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d.%m.%Y %H:%M')

        # Ustun nomlarini o'zbekchaga o'zgartirish
        columns_map = {
            'user_id': 'Telegram ID',
            'username': 'Username',
            'full_name': 'To\'liq ismi',
            'created_at': 'Ro\'yxatdan o\'tgan vaqti',
            'referrer_id': 'Taklif qiluvchi ID',
            'referrer_username': 'Taklif qiluvchi username',
            'ref_count': 'Taklif qilganlar soni',
            'is_active': 'Faol'
        }
        df = df.rename(columns=columns_map)

        # Excel fayl nomi
        filename = f"users_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
        filepath = f"data/files/{filename}"

        # Excel faylni yaratish
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Foydalanuvchilar', index=False)

            # Ustun kengliklarini moslash
            worksheet = writer.sheets['Foydalanuvchilar']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.column_dimensions[worksheet.cell(1, idx + 1).column_letter].width = max_length

        # Faylni yuborish
        excel_file = FSInputFile(filepath)
        await message.answer_document(
            document=excel_file,
            caption=(
                f"📊 Bot foydalanuvchilari ro'yxati:\n"
                f"📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"👥 Jami: {len(users):,} ta foydalanuvchi"
            )
        )

    except Exception as e:
        print(f"Error creating Excel file: {e}")
        await message.answer("❌ Excel fayl yaratishda xatolik yuz berdi")


@router.message(F.text == "⬅️ Orqaga", AdminFilter())
async def back_to_main(message: Message):
    await message.answer(
        "Asosiy menyuga qaytdingiz",
        reply_markup=main_keyboard
    )


@router.message(F.text == "⬅️ Orqaga", AdminFilter())
async def back_to_main(message: Message):
    await message.answer(
        "Asosiy menyuga qaytdingiz",
        reply_markup=main_keyboard
    )