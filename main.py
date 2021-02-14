from templatebot import Bot
from discord import Intents, AllowedMentions

from utils.loadcfg import load
from utils.database import DatabaseInterface

# Load the config file & set TOKEN to the token
try:
    config = load()
except FileNotFoundError:
    print("Config file not found, exiting.")
    exit()

# Make sure the token isn't empty/None
TOKEN = config.get("token")
if not TOKEN:
    print("No token provided, exiting.")
    exit()

# Create intents with just what we need
intents = Intents(
    guilds=True,
    members=True,
    messages=True,
    reactions=True,
)

# Custom prefix
async def get_prefix(bot, message):
    if not message.guild:
        p = config.get("prefix", "!")
    else:
        gconf = await bot.db.get_guild_config(message.guild.id)
        if not gconf:
            p = config.get("prefix", "!")
        else:
            p = gconf["prefix"]
    return p

# Create the bot itself
bot = Bot(
    name="ToxBot",
    command_prefix=get_prefix,
    intents=intents,
    allowed_mentions=AllowedMentions(replied_user=False, roles=False),
    help_command=None,
)
bot.VERSION = "V1.0.0-alpha"
bot.ENV = config.get("env", "prod")
bot.config = config
bot.db = DatabaseInterface(config, load("static/default.yml"))

# Load the cogs we need
bot.load_initial_cogs(
    "cogs.ui",
)

# Run the bot
bot.run(TOKEN)
