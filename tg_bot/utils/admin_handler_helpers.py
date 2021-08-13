from aiogram.types import Message
from tg_bot.services.db import Repo
from tg_bot.utils import text_templates as tt
from tg_bot.utils.misc import get_bot


async def mailing_sender(reciepients: list, text: str):
    bot = get_bot()

    for user in reciepients:
        await bot.send_message(chat_id=user["tg_id"], text=text)


async def _change_role(msg: Message, repo: Repo, role: str):
    try:
        username = msg.text.split(" ")[1]
    except IndexError:
        await msg.answer(
            text=tt.NO_USERNAME_MESSAGE,
        )
    else:
        users = await repo.users_list()
        usernames = [user["username"] for user in users]
        if username not in usernames:
            await msg.answer(
                text=tt.NO_USERNAME_IN_DB_MESSAGE,
            )
        else:
            await repo.change_user_role(username=username, role=role)

            await msg.answer(
                text=tt.ROLE_CHANGED_MESSAGE.format(username=username, role=role)
            )
