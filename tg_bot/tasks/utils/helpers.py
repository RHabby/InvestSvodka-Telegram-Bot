from functools import wraps
from typing import List, Optional, Union

from aiogram.types import InputFile
from aiogram.utils.exceptions import BotBlocked
from tg_bot.config import load_config
from tg_bot.services.db import Repo
from tg_bot.services.redis_service import get_list, get_value
from tg_bot.tasks.utils.db import get_db
from tg_bot.utils.handler_helpers import _collect_media_group
from tg_bot.utils.misc import get_bot


def init_db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not kwargs.get("repo"):
            config = load_config("bot.ini")
            db = get_db(config)
            repo = await db.__anext__()

            return await func(repo=repo, *args, **kwargs)

    return wrapper


async def _send_to_subscribers(service_name: str, repo: Repo) -> None:
    subscribers = await repo.get_subscribers(service_name=service_name)
    await _content_sender(subscribers=subscribers,
                          service_name=service_name,
                          repo=repo)


async def _content_sender(subscribers: List[int],
                          service_name: str,
                          repo: Repo) -> None:
    if subscribers:
        for subscriber in subscribers:
            try:
                await _send_by_path_type(chat_id=subscriber,
                                         service_name=service_name)
            except BotBlocked:
                await repo.mark_user_as_inactive(tg_id=int(subscriber))


async def _send_by_path_type(chat_id: int, service_name: str) -> None:
    bot = get_bot()
    path = get_image_path(service_name=service_name)

    if isinstance(path, bytes):
        await bot.send_photo(
            chat_id=int(chat_id),
            photo=InputFile(path.decode()),
            caption=f"#{service_name}",
        )
    else:
        if path:
            media = _collect_media_group(images=path)
            await bot.send_media_group(chat_id=int(chat_id), media=media)


def get_image_path(service_name: str) -> Union[Optional[bytes], List[bytes]]:
    if service_name == "all_base_template":
        return get_list(service_name)
    else:
        return get_value(service_name)
