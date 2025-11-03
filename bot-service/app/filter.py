from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from app.config import ADMIN_ID


class IsAdmin(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if str(update.from_user.id) == ADMIN_ID:
            return True
        return False
    

class IsRita(BaseFilter):
    def __init__(self, ids: list):
        self.ids = ids

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        if update.from_user.id in self.ids:
            return True
        return False