from disnake import RawMessageDeleteEvent
from disnake.ext.commands import Cog
from loguru import logger

from ...database import Message


class OnRawMessageDelete(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent) -> None:
        if any(
            [
                payload.channel_id in self.bot.config["ignored_channels"],
                payload.guild_id != self.bot.config["guild_id"],
            ]
        ):
            return

        await self.bot.sync_completed.wait()

        await Message.filter(id=payload.message_id).update(deleted=True)

        logger.info(f"Message {payload.message_id} marked as deleted.")
