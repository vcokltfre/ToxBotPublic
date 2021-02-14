from discord.ext import commands
from discord import Embed, TextChannel, Role
from templatebot import Bot

from utils.checks import noadmin


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

        if ctx.me.guild_permissions.administrator:
            embed.set_footer(text="Please remove admin from me.")

        await ctx.reply(embed=embed) # TODO: More info / stats here

    @commands.group(name="config")
    @commands.has_guild_permissions(manage_guild=True)
    @noadmin()
    async def config(self, ctx: commands.Context):
        pass

    @config.command(name="prefix")
    async def config_prefix(self, ctx: commands.Context, prefix: str = None):
        prefix = prefix or "!"

        if len(prefix) > 8:
            return await ctx.reply("Prefixes must be 8 characters or shorter.")

        # TODO: Database config logic

        await ctx.reply(f"The prefix for this server has been set to `{prefix}`")

    @config.command(name="logs")
    async def config_logs(self, ctx: commands.Context, channel: TextChannel = None):
        if channel:
            channel = ctx.guild.get_channel(channel.id)

            if not channel:
                return await ctx.reply("The channel provided is not in this server.")

        # TODO: Database config logic

        response = f"set to {channel.mention}" if channel else "removed"
        await ctx.reply(f"The log channel for this server has been {response}")

    @config.command(name="mute")
    async def config_muted_role(self, ctx: commands.Context, role: Role = None):
        if role:
            role = ctx.guild.get_role(role.id)

            if not role:
                return await ctx.reply("The role provided is not in this server.")

        if not ctx.me.guild_permissions.manage_roles:
            return await ctx.reply("I don't have the manage roles permission, so I can't assign roles.")

        if role >= ctx.me.top_role:
            return await ctx.reply("The role provided is above my tope role, so I can't assign it.")

        if role.managed:
            return await ctx.reply("The role provided is an integration role, so I can't assign it.")

        # TODO: Database config logic

        response = f"set to {role.mention}" if role else "removed"
        await ctx.reply(f"The muted role for this server has been {response}")


def setup(bot: Bot):
    bot.add_cog(UI(bot))