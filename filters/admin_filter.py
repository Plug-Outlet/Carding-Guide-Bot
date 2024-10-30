# filters/admin_filter.py

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.admin_utils import is_admin

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return is_admin(message.from_user.id, message.from_user.username)