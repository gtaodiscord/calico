import asyncio
import itertools
from time import time

import disnake
from asyncpg import UniqueViolationError
from disnake import Guild, member
from disnake.ext.commands import Cog
from loguru import logger
from more_itertools import chunked
from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from ..database import Category, Channel
from ..utils import config


class Sync(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def sync_channels(self, guild: Guild) -> None:
        """Syncs categories and channels to database."""
        logger.info("Category synchronisation starting...")

        start_time = time()

        for category in guild.categories:
            if category.id in self.bot.config["ignored_categories"]:
                continue

            try:
                await Category.create(id=category.id, name=category.name)
            except IntegrityError:
                await Category.filter(id=category.id).update(name=category.name)

            logger.info(f"Category {category.name}({category.id}) synced.")

            for channel in category.text_channels:
                if channel.id in self.bot.config["ignored_channels"]:
                    continue

                (staff := channel.id in self.bot.config["staff_channels"])
                try:
                    await Channel.create(
                        id=channel.id,
                        name=channel.name,
                        staff=staff,
                        category_id=channel.category_id,
                    )
                except IntegrityError:
                    await Channel.filter(id=channel.id).update(
                        name=channel.name, staff=staff, category_id=channel.category_id
                    )

                logger.info(f"Channel {channel.name}({channel.id}) synced.")
        end_time = time()

        logger.info(
            f"Syncronised all channels in database in {end_time - start_time:0.3f}s."
        )

    async def sync_users(self, guild: Guild) -> None:
        await guild.chunk()

        db = Tortoise.get_connection("default")

        total_synced_users = 0

        start_time = time()

        for members in chunked(guild.members, 1000):
            values = [
                [
                    member.id,
                    member.name,
                    member.discriminator,
                    member.created_at,
                    member.joined_at,
                    True,
                ]
                for member in members
            ]

            await db.execute_many(
                """
                INSERT INTO users (id, name, discriminator, created_at, joined_at, in_guild)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    discriminator = EXCLUDED.discriminator,
                    joined_at = EXCLUDED.joined_at,
                    in_guild = EXCLUDED.in_guild;
                """,
                values,
            )

            total_synced_users += len(members)
            logger.info(f"Synced {total_synced_users} total users.")

        end_time = time()

        logger.info(
            f"Syncronised a total of {total_synced_users} users to the database in {end_time - start_time:0.3f}s"
        )

    @Cog.listener()
    async def on_guild_available(self, guild: Guild) -> None:
        if guild.id != self.bot.config["guild_id"]:
            return

        await asyncio.gather(self.sync_channels(guild), self.sync_users(guild))

        self.bot.sync_completed.set()

    @Cog.listener()
    async def on_guild_unavailable(self, guild: Guild) -> None:
        if guild.id != self.bot.config["guild_id"]:
            return

        self.bot.sync_completed.clear()
