import asyncpg
from tg_bot.config import Config
from tg_bot.services.db import Repo


async def get_db(config: Config) -> asyncpg.Connection:
    conn = await asyncpg.connect(user=config.db.user, password=config.db.password,
                                 host=config.db.host, database=config.db.database)
    repo = Repo(conn)
    try:
        yield repo
    finally:
        await conn.close()
