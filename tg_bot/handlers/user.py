import typing

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, Message
import tg_bot.models.image as im
from tg_bot.services.db import Repo
from tg_bot.services.redis_service import get_list, get_value
from tg_bot.utils import kboards as kb
from tg_bot.utils import text_templates as tt
from tg_bot.utils.handler_helpers import (_available_services_data, _collect_media_group,
                                          _user_subscriptions_data)


# message handlers
async def user_start(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)
    await repo.add_user(
        tg_id=msg.from_user.id,
        username=msg.from_user.username
    )
    await msg.answer(
        text=tt.START_MESSAGE.format(msg.from_user.username),
        disable_web_page_preview=True
    )


async def help_user(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)
    await msg.answer(text=tt.HELP_MESSAGE)


async def get_base_indexes_image(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)

    image = get_value(im.IndexesImage.redis_key)
    if image:
        await msg.answer_photo(
            photo=InputFile(image.decode()),
            caption="#indexes"
        )


async def get_crypto_image(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)

    image = get_value(im.CryptoImage.redis_key)
    if image:
        await msg.answer_photo(
            photo=InputFile(image.decode()),
            caption="#crypto"
        )


async def get_tinkoff_etf_image(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)

    image = get_value(im.TinkoffETFImage.redis_key)
    if image:
        await msg.answer_photo(
            photo=InputFile(image.decode()),
            caption="#tinkoff_etf"
        )


async def get_user_info(msg: typing.Union[Message, CallbackQuery], repo: Repo) -> None:
    subs = await repo.get_user_subscriptions(tg_id=msg.from_user.id)

    if isinstance(msg, Message):
        cmd = msg.text.split(" ")[0].lstrip("/")
        await msg.answer(
            text=tt.USER_INFO_MESSAGE,
            reply_markup=kb.user_info_kboard(has_subscriptions=bool(subs)),
        )
    elif isinstance(msg, CallbackQuery):
        cmd = msg.data
        await msg.answer()
        await msg.message.edit_text(
            text=tt.USER_INFO_MESSAGE,
            reply_markup=kb.user_info_kboard(has_subscriptions=bool(subs)),
        )

    await repo.increase_interactions_counter(command=cmd)


async def get_all_images(msg: Message, repo: Repo) -> None:
    cmd = msg.text.split(" ")[0].lstrip("/")
    await repo.increase_interactions_counter(command=cmd)

    images = get_list("all_base_templates")
    media = _collect_media_group(images)
    await msg.answer_media_group(media=media)


async def echo(msg: Message, repo: Repo) -> None:
    await repo.increase_interactions_counter(command="echo")
    await msg.answer(text=tt.ECHO_MESSAGE.format(text=msg.text))


# callback handlers
async def user_subscriptions_callback(query: CallbackQuery, repo: Repo) -> None:
    await query.answer()

    data = await _user_subscriptions_data(user_id=query.from_user.id, repo=repo)
    await query.message.edit_text(
        text=data["text"],
        reply_markup=data["markup"]
    )


async def subscribe_to_service_callback(query: CallbackQuery, repo: Repo) -> None:
    await query.answer()
    data = await _available_services_data(user_id=query.from_user.id, repo=repo)

    await query.message.edit_text(
        text=data["text"],
        reply_markup=data["markup"],
    )


async def subscribe_callback(query: CallbackQuery,
                             callback_data: typing.Dict[str, typing.Union[str, int]],
                             repo: Repo) -> None:
    await query.answer()
    await repo.add_subcription(tg_id=query.from_user.id,
                               service_id=int(callback_data["service_id"]))

    data = await _available_services_data(user_id=query.from_user.id, repo=repo)
    await query.message.edit_text(text=data["text"], reply_markup=data["markup"])


async def unsubscribe_callback(query: CallbackQuery,
                               callback_data: typing.Dict[str, typing.Union[str, int]],
                               repo: Repo) -> None:
    await query.answer()
    await repo.delete_subscription(tg_id=query.from_user.id,
                                   service_id=int(callback_data["service_id"]))

    data = await _user_subscriptions_data(user_id=query.from_user.id, repo=repo)
    await query.message.edit_text(
        text=data["text"],
        reply_markup=data["markup"],
    )


# service function
def register_user(dp: Dispatcher) -> None:
    """Register handlers for regular user"""
    # message handlers
    dp.register_message_handler(user_start,
                                commands=["start"], state="*")
    dp.register_message_handler(help_user,
                                commands=["help"], state="*")
    dp.register_message_handler(get_base_indexes_image,
                                commands=["indexes"], state="*")
    dp.register_message_handler(get_crypto_image,
                                commands=["crypto"], state="*")
    dp.register_message_handler(get_tinkoff_etf_image,
                                commands=["tinkoff_etf"], state="*")
    dp.register_message_handler(get_user_info,
                                commands=["user"], state="*")
    dp.register_message_handler(get_all_images,
                                commands=["all"], state="*")
    dp.register_message_handler(echo, state="*")

    # callback handlers
    dp.register_callback_query_handler(get_user_info,
                                       lambda query: query.data == "user",
                                       state="*")
    dp.register_callback_query_handler(user_subscriptions_callback,
                                       lambda query: query.data == "subscriptions",
                                       state="*")
    dp.register_callback_query_handler(subscribe_to_service_callback,
                                       lambda query: query.data == "services",
                                       state="*")
    dp.register_callback_query_handler(subscribe_callback,
                                       kb.action_w_services_cb.filter(action="subscribe"),
                                       state="*")
    dp.register_callback_query_handler(unsubscribe_callback,
                                       kb.action_w_services_cb.filter(action="unsubscribe"),
                                       state="*")
