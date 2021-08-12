import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    """Tgbot credentials."""

    token: str
    admin_id: int
    use_redis: bool


@dataclass
class DbConfig:
    """Database credentials."""

    user: str
    password: str
    host: str
    database: str


@dataclass
class Config:
    """Main config class."""

    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    """Cast boolean value."""
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str) -> Config:
    """Read and load config function."""
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
            use_redis=cast_bool(tg_bot["use_redis"]),
        ),
        db=DbConfig(**config["db"]),
    )
