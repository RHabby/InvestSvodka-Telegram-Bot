from aiogram import Bot
from tg_bot.config import load_config


def get_bot() -> Bot:
    config = load_config("bot.ini")
    return Bot(token=config.tg_bot.token)
