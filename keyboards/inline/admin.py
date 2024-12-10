from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from data.texts import button


def create_admin_button(callback_data: str) -> InlineKeyboardButton:
    """Create a single admin button with text from button() function"""
    return InlineKeyboardButton(
        text=button(callback_data),
        callback_data=callback_data
    )


def get_admin_main_menu() -> InlineKeyboardBuilder:
    """Create main admin menu keyboard"""
    builder = InlineKeyboardBuilder()

    # Add buttons one by one vertically
    builder.row(create_admin_button("admin_send_message"))
    builder.row(create_admin_button("admin_statistics"))

    return builder.as_markup()


def get_admin_back_menu() -> InlineKeyboardBuilder:
    """Create admin back menu keyboard"""
    builder = InlineKeyboardBuilder()
    builder.row(create_admin_button("admin_back"))
    return builder.as_markup()


# Create keyboard instances
admin_main_menu = get_admin_main_menu()
admin_back_menu = get_admin_back_menu()


# If you need a more flexible approach with multiple buttons:
def create_admin_keyboard(*button_data: str) -> InlineKeyboardBuilder:
    """Create keyboard with multiple buttons"""
    builder = InlineKeyboardBuilder()

    for data in button_data:
        builder.row(create_admin_button(data))

    return builder.as_markup()


# Example usage:
"""
custom_keyboard = create_admin_keyboard(
    "admin_users",
    "admin_settings",
    "admin_back"
)
"""