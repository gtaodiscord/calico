from .on_member_join import OnMemberJoin
from .on_member_remove import OnMemberRemove
from .on_member_update import OnMemberUpdate
from .on_message import OnMessage
from .on_raw_bulk_message_delete import OnRawBulkMessageDelete
from .on_raw_message_delete import OnRawMessageDelete


def setup(bot) -> None:
    bot.add_cog(OnMemberJoin(bot))
    bot.add_cog(OnMemberRemove(bot))
    bot.add_cog(OnMemberUpdate(bot))
    bot.add_cog(OnMessage(bot))
    bot.add_cog(OnRawBulkMessageDelete(bot))
    bot.add_cog(OnRawMessageDelete(bot))
