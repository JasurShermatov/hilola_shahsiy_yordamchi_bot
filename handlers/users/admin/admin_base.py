from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from data.texts import text
from filters.admin import AdminFilter
from keyboards.inline.admin import admin_main_menu


router = Router()


@router.message(AdminFilter(), Command("admin"), StateFilter("*"))
@router.callback_query(AdminFilter(), F.data == "admin_back", StateFilter("*"))
async def admin_start(event: Union[Message, CallbackQuery], state: FSMContext):
    fullname = event.from_user.full_name
    admin_text = text("admin_start").format(fullname=fullname)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=admin_text,
            reply_markup=admin_main_menu
        )
    else:
        await event.answer(
            text=admin_text,
            reply_markup=admin_main_menu
        )

    await state.clear()
