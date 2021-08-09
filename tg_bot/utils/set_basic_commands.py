from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher


async def set_basic_commands(dp: Dispatcher) -> None:
    """Set basic commands for the bot"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "Help message"),
            types.BotCommand("indexes", "indexes image"),
            types.BotCommand("crypto", "crypto image"),
            types.BotCommand("tinkoff_etf", "tinkoff etf image"),
            types.BotCommand("user", "user options"),
        ],
    )
