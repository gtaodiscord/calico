from .config import load_config
from .sync import Sync

__all__ = "load_config"


def setup(bot) -> None:
    bot.add_cog(Sync(bot))
