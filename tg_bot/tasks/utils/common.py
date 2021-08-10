from typing import Type

from tg_bot.models.image import BaseTemplateImage
from tg_bot.services import stock_obtainer as stock
from tg_bot.services.db import Repo
from tg_bot.services.image_processor import create_image
from tg_bot.services.redis_service import set_value
from tg_bot.tasks.utils.helpers import _send_to_subscribers, init_db


def create_image_task(image_config: Type[BaseTemplateImage]) -> None:
    """Задача по генерации изображения

    генерирует изображение по основному шаблону
    по полученным данным и сохраняет путь до изображения
    в редис
    """
    ticks = stock.get_tickers(ticker_list=image_config.tickers)

    image = create_image(tickers=ticks,
                         image_config=image_config)

    set_value(image_config.redis_key, image)


@init_db
async def send_to_subscribers_task(repo: Repo) -> None:
    services = await repo.get_service_names()

    for service in services:
        await _send_to_subscribers(service_name=service, repo=repo)
