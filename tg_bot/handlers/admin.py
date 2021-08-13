from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from tg_bot.models.role import UserRole
from tg_bot.services.db import Repo
from tg_bot.utils import admin_kboards as ak
from tg_bot.utils import text_templates as tt
from tg_bot.utils.admin_handler_helpers import _change_role, mailing_sender


# message handlers
async def admin_cmd(msg: Message):
    await msg.answer(
        text=tt.MAIN_ADMIN_MESSAGE,
        reply_markup=ak.admin_kboard()
    )


async def make_admin_cmd(msg: Message, repo: Repo):
    await _change_role(msg=msg, repo=repo, role="admin")


async def make_user_cmd(msg: Message, repo: Repo):
    await _change_role(msg=msg, repo=repo, role="user")


async def mailing_cmd(msg: Message, repo: Repo):
    try:
        text = msg.text.split("\n")[1]
    except IndexError:
        await msg.answer(
            text=tt.NO_TEXT_MESSAGE,
        )
    else:
        users = await repo.users_list()
        await mailing_sender(recipients=users, text=text)


# callback handlers
async def interactions_stats(query: CallbackQuery, repo: Repo):
    await query.answer()

    stats = await repo.get_interactions_stats()

    text = tt.CMD_STATS_MESSAGE
    for stat in stats:
        text += tt.ADD_TO_CMD_STATS.format(command=stat["command"], cnt=stat["cnt"])

    await query.message.answer(text=text)


async def bot_users(query: CallbackQuery, repo: Repo):
    await query.answer()

    users = await repo.users_list()
    users_cnt = len(users)
    active_users = len([user for user in users if user["is_active"]])
    active_users_percent = (active_users / users_cnt) * 100

    text = tt.USERS_STATS_MESSAGE.format(users_cnt=users_cnt,
                                         active_users=active_users,
                                         active_users_percent=active_users_percent)
    for user in users[:50]:
        text += tt.ADD_TO_USERS_STATS.format(username=user["username"],
                                             tg_id=user["tg_id"],
                                             is_active=user["is_active"])

    await query.message.answer(text=text)


async def services_stats(query: CallbackQuery, repo: Repo):
    await query.answer()

    services = await repo.get_services_stats()

    text = tt.SERVICES_STATS_MESSAGE
    for service in services:
        text += tt.ADD_TO_SERVICEC_STATS.format(service_name=service["service_name"],
                                                subscribers=service["subscribers"])

    await query.message.answer(text=text)


# service function
def register_admin(dp: Dispatcher):
    # register message handlers
    dp.register_message_handler(admin_cmd,
                                commands=["admin"],
                                state="*",
                                role=UserRole.ADMIN)
    dp.register_message_handler(make_admin_cmd,
                                commands=["make_admin"],
                                state="*",
                                role=UserRole.ADMIN)
    dp.register_message_handler(make_user_cmd,
                                commands=["make_user"],
                                state="*",
                                role=UserRole.ADMIN)
    dp.register_message_handler(mailing_cmd,
                                commands=["mailing"],
                                state="*",
                                role=UserRole.ADMIN)

    # register callback handlers
    dp.register_callback_query_handler(interactions_stats,
                                       lambda query: query.data == "interaction_stats",
                                       state="*")
    dp.register_callback_query_handler(bot_users,
                                       lambda query: query.data == "bot_users",
                                       state="*")
    dp.register_callback_query_handler(services_stats,
                                       lambda query: query.data == "services_stats",
                                       state="*")
