from discord.ext import commands
from discord import Message
from templatebot import Bot
from time import time


class Detector(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def logsend(self, guild: int, **kwargs):
        gconf = await self.bot.db.get_guild_config(guild)

        if not gconf:
            return

        channelid = gconf["logs"]

        if not channelid:
            return

        channel = self.bot.get_channel(channelid)

        if not channel:
            return

        await channel.send(**kwargs)

    async def should_ignore(self, message: Message):
        if message.author == self.bot.user:
            return True, "Ignoring self"

        if not message.guild:
            return True, "Ignoring DM"

        gconf = await self.bot.db.get_guild_config(message.guild.id)
        if not gconf:
            return True, "No guild config"

        ignore = gconf["ignore"]

        if message.author.id in ignore["users"]:
            return True, "Ignoring user"

        if message.channel.id in ignore["channels"]:
            return True, "Ignoring channel"

        if message.channel.category and message.channel.category.id in ignore["categories"]:
            return True, "Ignoring category"

        roles = set(ignore["roles"])
        member_roles = set(message.author.roles)

        if roles & member_roles:
            return True, "Ignoring roles"

        if message.author.bot and ignore["bots"]:
            return True, "Ignoring bots"

        if message.author.guild_permissions.manage_messages and ignore["mods"]:
            return True, "Ignoring mods"

        return False, None

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        res = await self.should_ignore(message)
        if res[0]:
            print(message.id, message.author.id, res[1])
            return

        guildreq = self.bot.db.guildreqs[message.guild.id]

        if guildreq["today"] >= guildreq["limit"]:
            if not guildreq["sent"]:
                await self.logsend(message.guild.id, content="Daily request limit exceeded.")
                await self.bot.db.limit_sent(message.guild.id)
            return

        ts = time()
        results = await self.bot.api.request(message.content)
        et = round(time() - ts, 4)

        self.bot.times.add(et)
        print(self.bot.times.avg())

        print(et, results)
        await self.bot.db.add_request(message.guild.id)


def setup(bot: Bot):
    bot.add_cog(Detector(bot))