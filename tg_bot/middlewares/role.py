from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tg_bot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    """User role middleware."""

    skip_patterns = ["error", "update"]

    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def pre_process(self, obj, data, *args):
        """Before action"""
        repo = data["repo"]
        admins = await repo.admins_list()

        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif obj.from_user.id in admins:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        """After action"""
        del data["role"]
