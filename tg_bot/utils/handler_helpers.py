import typing

from aiogram.types import InlineKeyboardMarkup, InputFile, MediaGroup
from tg_bot.services.db import Repo
from tg_bot.utils import kboards as kb
from tg_bot.utils import text_templates as tt


async def _available_services_data(
        user_id: int,
        repo: Repo) -> typing.Dict[str, typing.Optional[InlineKeyboardMarkup]]:
    """Cast text and markup for available services to subscribe"""
    available_services = await repo.get_available_services_to_subscribe(tg_id=user_id)

    if available_services:
        text = tt.AVAILABLE_SERVICES_MESSAGE
        markup = kb.generate_services_markup(
            services=available_services,
            action="subscribe",
        )
    else:
        text = tt.ALREADY_SUBSCRIBED_MESSAGE
        markup = None

    return {"text": text, "markup": markup}


async def _user_subscriptions_data(
        user_id: int,
        repo: Repo) -> typing.Dict[str, typing.Optional[InlineKeyboardMarkup]]:
    """Cast text and markup by user subscribtions"""
    subs = await repo.get_user_subscriptions(tg_id=user_id)

    if subs:
        text = tt.UNSUBSCRIBE_MESSAGE
        markup = kb.generate_services_markup(
            services=subs,
            action="unsubscribe",
        )
    else:
        text = tt.ALREDY_UNSUBSCRIBED_MESSAGE
        markup = None

    return {"text": text, "markup": markup}


def _collect_media_group(images: typing.List[bytes]) -> MediaGroup:
    media = MediaGroup()
    for image in images:
        media.attach_photo(InputFile(image.decode()))

    return media
