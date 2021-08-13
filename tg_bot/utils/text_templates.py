# user text templates
START_MESSAGE = (
    "Привет, {}! \n\n"
    "Я — бот, информирующий тебя о котировках на различных рынках. "
    "Я получаю информацию из сервиса "
    "<a href='https://finance.yahoo.com'>Yahoo Finance</a> и, "
    "на основании полученных данных, "
    "генерирую изображения с различными подборками.\n\n"
    "В настоящий момент доступны:\n"
    "— Базовые Индексы;\n"
    "— ETF Тиньков Банка; \n"
    "— Криптовалюты.\n\n"
    "Совсем скоро должны появиться ETF от Finex.\n\n"
    "Вот, что я умею:\n"
    "— генерировать изображения с котировками по нескольким подборкам "
    "(количество будет увеличиваться);\n"
    "— рассылать котировки по выбранным подборкам, или всем сразу, дважды в день "
    "(утром и вечером);\n\n"
    "Чтобы попробовать, обратись к команде /help"
)
HELP_MESSAGE = (
    "Вот список доступных команд:\n"
    "/help — показывает это сообщение;\n"
    "/indexes — подборка с основными индексами:\n"
    "      • SnP500;\n"
    "      • Nasdaq;\n"
    "      • Dow Jones;\n"
    "      • Moex;\n"
    "      • RTS,\n"
    "      • VIX;\n"
    "   и курсами валют:\n"
    "      • USD/RUB;\n"
    "      • EUR/RUB;\n"
    "      • BTC/USD.\n"
    "/crypto — подборка с курсами криптовалют:\n"
    "      • BTC — Bitcoin;\n"
    "      • ETH — Etherium;\n"
    "      • BNB — Binance Coin;\n"
    "      • DOGE — Dogecoin;\n"
    "      • XRP — Ripple;\n"
    "      • DOT — Polkadot;\n"
    "      • ADA — Cardano;\n"
    "      • LTC — Litecoin;\n"
    "      • UNI — Uniswap.\n"
    "/tinkoff_etf — ETF Тинькофф:\n"
    "      • TIPO — Тинькофф Индекс IPO;\n"
    "      • TGLD — Тинькофф Золото;\n"
    "      • TSPX — Тинькофф S&P 500;\n"
    "      • TECH — Тинькофф NASDAQ;\n"
    "      • TBIO — Тинькофф NASDAQ Biotech;\n"
    "      • TMOS — Тинькофф iMOEX;\n"
    "      • TSPV — Тинькофф SPAC;\n"
    "      • TGRN — Тинькофф Green Economy;\n"
    "      • TBRU — Тинькофф Bonds RUB.\n"
    "/user — доступные опции для пользователя "
    "(подписаться на рассылку, отписаться от рассылки).\n\n"
    "Если в этом списке появятся новые команды — я дам тебе знать."
)

TICKERS_COLLECTION_MESSAGE = ""

USER_INFO_MESSAGE = (
    "Здесь можно подписаться на ежедневную рассылку с интересующей "
    "тебя подборкой. А еще можно отписаться.\n\n"
    "Когда в списке опций появятся новые команды — я дам тебе знать."
)

ECHO_MESSAGE = "Не понимаю о чем ты: '{text}'"

AVAILABLE_SERVICES_MESSAGE = (
    "Чтобы подписаться нажми на кнопку с названием подборки.\n\n"
    "Обрати внимание, что в списке нет подборок, на которые уже есть подписаны.\n\n"
    "Доступно для подписки:"
)
ALREADY_SUBSCRIBED_MESSAGE = "Похоже, что ты подписан на все доступные подборки."

UNSUBSCRIBE_MESSAGE = "Чтобы отписаться нажми на кнопку с названием подборки.\n\nТвои подписки:"
ALREDY_UNSUBSCRIBED_MESSAGE = "Похоже, подписки кончились."

# admin text templates
MAIN_ADMIN_MESSAGE = (
    "Доступные команды:\n"
    "/admin — выводит это сообщение;\n"
    "/make_admin — изменяет роль пользователя на admin."
    "Формат использования: <code>/make_admin username</code>\n"
    "/make_user — изменяет роль пользователя на user."
    "Формат использования: <code>/make_user username</code>\n"
    "/mailing — команда для рассылки всем пользователям бота. "
    "Формат использования: <code>/mailing //перенос на новую строку// "
    "Сообщение для рассылки</code>.\n\n"
    "Статистика:"
)

NO_USERNAME_MESSAGE = "Похоже, что username не передан."

NO_USERNAME_IN_DB_MESSAGE = "Похоже, что такого юзера нет в базе."

ROLE_CHANGED_MESSAGE = "Роль пользователя '{username}' изменена на '{role}'"

NO_TEXT_MESSAGE = "Похоже, нет текста для рассылки."

CMD_STATS_MESSAGE = "Статистика использования команд бота:\n"
ADD_TO_CMD_STATS = " • <code>{command}</code> — <strong>{cnt}</strong>;\n"

USERS_STATS_MESSAGE = (
    "Пользователи бота: <code>{users_cnt}</code> (показаны первые 50)\n"
    "Активных пользователей (<b>незаблокировавших бота</b>): "
    "<code>{active_users} ({active_users_percent}%)</code>\n\n"
    "<b>Username</b> : <b>Telegram ID</b> : <b>is_active</b>\n"

)
ADD_TO_USERS_STATS = (
    " • <i>@{username}</i> : "
    "<code>{tg_id}</code> : "
    "<b>{is_active}</b>\n"
)

SERVICES_STATS_MESSAGE = (
    "Статистика сервисов:\n"
    "<b>Service</b> — <b>Subscribers</b>\n"
)

ADD_TO_SERVICEC_STATS = (
    " • <code>{service_name}</code> — "
    "<b><i>{subscribers}</i></b>\n"
)
