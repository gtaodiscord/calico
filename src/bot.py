import asyncio
from os import environ
from random import choice

from disnake import Game
from disnake.ext.commands import Bot
from disnake.ext.tasks import loop
from loguru import logger

from .database import db_init
from .utils import load_config

extensions = ["src.utils", "src.exts.events"]


class Calico(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="//", activity=Game("Sweet Baby Rays"), *args, **kwargs)

        self.config = load_config()

        self.sync_completed = asyncio.Event()

        for extension in extensions:
            self.load_extension(extension)
            logger.info(f"Loaded {extension}")

    @staticmethod
    async def on_ready() -> None:
        logger.info("Bot is ready.")

    def startup(self) -> None:
        self.loop.run_until_complete(db_init())

    def run(self) -> None:
        logger.info("Bot is starting...")
        super().run(environ["BOT_TOKEN"])
