# data/config.py
from environs import Env
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int


@dataclass
class TgBot:
    token: str
    channel_id: str
    channel_url: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Config:
    bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    try:
        admin_ids = list(map(int, env.list("ADMIN_IDS", default=[])))
    except ValueError:
        admin_ids = []

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            channel_id=env.str("CHANNEL_ID"),
            channel_url=env.str("CHANNEL_URL"),
            admin_ids=admin_ids,
            use_redis=env.bool("USE_REDIS", default=False),
        ),
        db=DbConfig(
            host=env.str("DB_HOST"),
            password=env.str("DB_PASS"),
            user=env.str("DB_USER"),
            database=env.str("DB_NAME"),
            port=env.int("PORT", default=6379),
        ),
    )
