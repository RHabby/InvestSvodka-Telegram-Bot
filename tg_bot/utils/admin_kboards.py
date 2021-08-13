from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_kboard():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton("Статистика использования команд",
                             callback_data="interaction_stats"),
        InlineKeyboardButton("Пользователи",
                             callback_data="bot_users"),
        InlineKeyboardButton("Сервисы",
                             callback_data="services_stats")
    )

    return markup
