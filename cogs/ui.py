from discord.ext import commands
from discord import Embed
from templatebot import Bot


class UI(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="about")
    @commands.has_guild_permissions(manage_messages=True)
    async def about(self, ctx: commands.Context):
        ver = self.bot.VERSION
        gc = len(self.bot.guilds)
        mc = sum([g.member_count for g in self.bot.guilds])

        desc = f"Creator: vcokltfre#6868\nVersion: {ver}\nGuilds: {gc}\nMembers: {mc}"
        embed = Embed(title=f"{self.bot.name} Info", colour=0x87ceeb, description=desc)

        await ctx.reply(embed=embed) # TODO: More info / stats here


def setup(bot: Bot):
    bot.add_cog(UI(bot))