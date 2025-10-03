# --== Setup ==-- #
import os
import logging

from typing import Final, Optional
from dotenv import load_dotenv

import discord
from discord.ext import commands

# --== Constants ==-- #
GUILD_ID: Final[int] = 710461772280102944
POINTS_BOT_ID: Final[int] = 484395597508509697


# --== Logging ==-- #
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)


# --== Environment Setup ==-- #

# README:
# This section is used to declare the bot's token, which allows it to run
# For obvious security reasons, the .env and my copy of the token cannot be found on the Git repository
# To use this bot, you'll need to get your own token and create your own .env file
# To make life easier, you can copy and paste the following line into the .env
# BOT_TOKEN="TOKEN_HERE" #Replace TOKEN_HERE with your token, remove the hashtag at the start

load_dotenv()
TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not found in .env file!")


# --== Discord and Bot Setup ==-- #
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="/", intents=intents)


# --== Caches ==--
guild: Optional[discord.Guild] = None
pointsBot: Optional[discord.Member] = None


# --== Helper Functions ==-- #
async def cache_points_bot() -> bool:
    global guild, pointsBot

    try:
        guild = await bot.fetch_guild(GUILD_ID)
    except discord.NotFound:
        log.warning(f"Guild with ID {GUILD_ID} could not be found.")
        return False
    except discord.DiscordException as e:
        log.error(f"Attempt to fetch guild {GUILD_ID} threw exception {e}")
        return False

    pointsBot = guild.get_member(POINTS_BOT_ID)
    if not pointsBot:
        log.warning(f"Points bot (ID: {POINTS_BOT_ID}) could not be found in guild {GUILD_ID}.")
        return False

    log.info(f"Points bot fetched: {pointsBot}")
    return True


# --== Events ==-- #
@bot.event
async def on_ready():
    log.info(f"Connected as {bot.user} (ID: {bot.user.id})")
    success = await cache_points_bot()
    if not success:
        log.warning("Failed to initialise points bot.")


# --== Activation ==-- #
def main() -> None:
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        log.info("Disconnected via manual interrupt.")
    except Exception as e:
        log.exception(f"Unexpected error during startup: {e}")


if __name__ == "__main__":
    main()