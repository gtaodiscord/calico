from os import environ

from dotenv import load_dotenv
from loguru import logger
from tortoise import Tortoise

load_dotenv()

TORTOISE_CONFIG = {
    "connections": {"default": environ["DB_URL"]},
    "apps": {
        "models": {
            "models": ["src.database.models"],
            "default_connection": "default",
        },
    },
}


async def db_init():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas()

    logger.info("Succesfully connected to database.")