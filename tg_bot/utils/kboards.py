from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import asyncpg


def user_info_kboard(has_subscriptions: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    if has_subscriptions:
        markup.add(
            InlineKeyboardButton("Подписки", callback_data="subscriptions"),
        )

    markup.add(
        InlineKeyboardButton("Подписаться", callback_data="services"),
    )

    return markup


action_w_services_cb = CallbackData("service", "action", "service_id")


def generate_services_markup(services: List[asyncpg.Record],
                             action: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for service in services:
        markup.add(
            InlineKeyboardButton(
                text=service["service_name"],
                callback_data=action_w_services_cb.new(
                    action=action,
                    service_id=service["id"]
                )
            )
        )
    markup.add(InlineKeyboardButton("Назад", callback_data="user"))

    return markup
