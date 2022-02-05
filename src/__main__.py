import disnake
from dotenv import load_dotenv

from .bot import Calico

load_dotenv()

intents = disnake.Intents(
    guilds=True,
    members=True,
    bans=False,
    emojis=False,
    integrations=False,
    webhooks=False,
    invites=False,
    voice_states=False,
    presences=False,
    messages=True,
    reactions=False,
    typing=False,
)


def main() -> None:
    bot = Calico(intents=intents)
    bot.startup()
    bot.run()


if __name__ == "__main__":
    main()
