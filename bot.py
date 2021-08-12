import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
import asyncpg
from tg_bot.config import load_config
from tg_bot.handlers import user
from tg_bot.middlewares.db import DbMiddleware
from tg_bot.utils.set_basic_commands import set_basic_commands

logger = logging.getLogger(__name__)


async def create_pool(user: str, password: str, database: str, host: str) -> asyncpg.Pool:
    """Create pool."""
    pool = await asyncpg.create_pool(
        user=user,
        password=password,
        host=host,
        database=database,
    )
    return pool


async def main() -> None:
    """Main bot function.

    Configure and start long polling
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting the bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
    )

    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=storage)

    dp.middleware.setup(DbMiddleware(pool))

    user.register_user(dp)
    await set_basic_commands(dp)

    try:
        await dp.start_polling(allowed_updates=False)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped")
