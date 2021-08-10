import asyncio

from celery import Celery
from celery.schedules import crontab
from pytz import timezone
import tg_bot.models.image as im
from tg_bot.tasks.utils.common import create_image_task, send_to_subscribers_task


app = Celery("tasks", broker="redis://localhost:6379/2")

app.conf.beat_schedule = {
    "indexes-every-three-minutes": {
        "task": "generate_indexes_image",
        "schedule": crontab(minute="*/3"),
    },
    "crypto-every-three-minutes": {
        "task": "generate_cryptos_image",
        "schedule": crontab(minute="*/3"),
    },
    "tinkoff-every-three-minutes": {
        "task": "generate_tinkoff_image",
        "schedule": crontab(minute="*/3"),
    },
    "send-to-subscribers": {
        "task": "send_to_subscribers",
        "schedule": crontab(minute="15", hour="10, 21")
    }
}
app.conf.timezone = timezone("Europe/Moscow")


@app.task(name="generate_indexes_image")
def generate_indexes_image() -> None:
    create_image_task(image_config=im.IndexesImage)


@app.task(name="generate_cryptos_image")
def generate_cryptos_image() -> None:
    create_image_task(image_config=im.CryptoImage)


@app.task(name="generate_tinkoff_image")
def generate_tinkoff_image() -> None:
    create_image_task(image_config=im.TinkoffETFImage)


@app.task(name="send_to_subscribers")
def send_to_subscribers() -> None:
    asyncio.run(send_to_subscribers_task())
