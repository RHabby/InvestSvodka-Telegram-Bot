from typing import Any, Dict, Union

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message
import asyncpg
from tg_bot.services.db import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    """Db Middleware"""

    skip_patterns = ["error", "update"]

    def __init__(self, pool: asyncpg.Pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj: Union[Message, CallbackQuery],
                          data: Dict, *args: Any) -> None:
        """Before action"""
        db = await self.pool.acquire()

        data["db"] = db
        data["repo"] = Repo(db)

    async def post_process(self, obj: Union[Message, CallbackQuery],
                           data: Dict, *args: Any) -> None:
        """After action"""
        del data["repo"]
        db = data.get("db")

        if db:
            await db.close()
