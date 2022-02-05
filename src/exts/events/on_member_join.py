from disnake import Member
from disnake.ext.commands import Cog
from loguru import logger
from tortoise.exceptions import IntegrityError

from ...database import User


class OnMemberJoin(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id != self.bot.config["guild_id"]:
            return

        await self.bot.sync_completed.wait()

        try:
            await User.create(
                id=member.id,
                name=member.name,
                discriminator=member.discriminator,
                created_at=member.created_at,
                joined_at=member.joined_at,
                in_guild=True,
            )
        except IntegrityError:
            await User.filter(id=member.id).update(
                name=member.name,
                discriminator=member.discriminator,
                created_at=member.created_at,
                joined_at=member.joined_at,
                in_guild=True,
            )

        logger.info(
            f"Member {member.name}#{member.discriminator}({member.id}) joined the guild."
        )
