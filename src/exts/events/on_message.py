from disnake import Message as DiscordMessage
from disnake.ext.commands import Cog
from loguru import logger

from ...database import Message


class OnMessage(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: DiscordMessage) -> None:
        if any(
            [
                message.author.bot,
                not message.guild,
                message.guild.id != self.bot.config["guild_id"],
                message.channel.id in self.bot.config["ignored_channels"],
                message.channel.category_id in self.bot.config["ignored_categories"],
            ]
        ):
            return

        await self.bot.sync_completed.wait()

        await Message.create(
            id=message.id,
            created_at=message.created_at,
            channel_id=message.channel.id,
            author_id=message.author.id,
        )

        logger.info(f"Message {message.id} added to the database.")
