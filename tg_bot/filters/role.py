from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from tg_bot.models.role import UserRole


class RoleFilter(BoundFilter):
    """User role filter"""

    key = "role"

    def __init__(self, role=None):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def check(self, obj):
        """Check user role"""
        if self.roles is None:
            return True
        data = ctx_data.get()
        return data.get("role") in self.roles
