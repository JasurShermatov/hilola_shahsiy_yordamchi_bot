# filters/reply_filters.py

from aiogram.filters import Filter
from aiogram.types import Message
from typing import Union


class ButtonFilter(Filter):
    def __init__(self, button_text: Union[str, list[str]]) -> None:
        self.button_text = button_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.button_text


# Asosiy menu button filterlari
class MyFriendsFilter(ButtonFilter):
    def __init__(self):
        super().__init__("👥 DO'STLARIM")


class StatisticsFilter(ButtonFilter):
    def __init__(self):
        super().__init__("📊 STATISTIKA")


class GameRulesFilter(ButtonFilter):
    def __init__(self):
        super().__init__("🏆 O'YIN SHARTLARI")


class ReferralLinkFilter(ButtonFilter):
    def __init__(self):
        super().__init__("♻️ REFERAL LINKNI OLISH")


class MyGiftsFilter(ButtonFilter):
    def __init__(self):
        super().__init__("🎁 MENING SOVG'ALARIM")


class ContactAdminFilter(ButtonFilter):
    def __init__(self):
        super().__init__("💭 ADMIN BILAN BOG'LANISH")
