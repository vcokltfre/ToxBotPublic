from templatebot import Bot
from discord import Intents

from utils.loadcfg import load

# Load the config file & set TOKEN to the token
try:
    config = load()
except FileNotFoundError:
    print("Config file not found, exiting.")
    exit()

# Make sure the token isn't empty/None
TOKEN = config.get('token')
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

# Create the bot itself
bot = Bot(name="ToxBot", command_prefix=config.get("prefix", "!"), intents=intents)

# Load the cogs we need
bot.load_initial_cogs()

# Run the bot
bot.run(TOKEN)