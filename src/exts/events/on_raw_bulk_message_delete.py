from disnake import RawBulkMessageDeleteEvent
from disnake.ext.commands import Cog
from loguru import logger

from ...database import Message


class OnRawBulkMessageDelete(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_bulk_message_delete(
        self, payload: RawBulkMessageDeleteEvent
    ) -> None:
        if any(
            [
                payload.channel_id in self.bot.config["ignored_channels"],
                payload.guild_id != self.bot.config["guild_id"],
            ]
        ):
            return

        await self.bot.sync_completed.wait()

        for message_id in payload.message_ids:
            await Message.filter(id=message_id).update(deleted=True)

            logger.info(f"Message {message_id} marked as deleted.")
