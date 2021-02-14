from discord.ext import commands
from discord import Embed, TextChannel, Role, CategoryChannel
from templatebot import Bot
from re import compile
from copy import copy

from utils.checks import noadmin

ID = compile(r"\b\d{17,20}\b")

def strset(data: set):
    return {str(i) for i in data}


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

        gconf = await self.bot.db.get_guild_config(ctx.guild.id)
        gconf["prefix"] = prefix
        await self.bot.db.set_guild_config(ctx.guild.id, gconf)

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

    @commands.command(name="setup")
    @commands.has_guild_permissions(manage_guild=True)
    @noadmin()
    async def guild_setup(self, ctx: commands.Context):
        BASE = f"Setting up server: {ctx.guild}\n\n"

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        exists = await self.bot.db.get_guild(ctx.guild.id)
        if exists:
            return await ctx.reply("This guild has already been set up!")

        # Prefix setting
        reply = await ctx.reply(BASE + "Enter a prefix (enter 'none' to use the default, '!')")

        response = await self.bot.wait_for("message", check=check, timeout=30)
        if len(response.content) > 8:
            return await reply.edit(content="Prefixes must be 8 characters long or fewer. Please run setup again.")
        prefix = response.content if response.content != "none" else "!"
        await response.delete()

        # Ignore lists
        await reply.edit(content=BASE + "Enter a list of IDs to ignore in the format `id1 id2 id3`. These can be user, role, channel or category IDs. I will resolve them automatically. Enter 'none' to not ignore any IDs.")

        response = await self.bot.wait_for("message", check=check, timeout=30)

        users, roles, channels, categories, rejected = set(), set(), set(), set(), set()
        if response.content != "none":

            results = [int(i) for i in ID.findall(response.content)]

            for result in results:
                if ctx.guild.get_member(result):
                    users.add(result)
                elif ctx.guild.get_role(result):
                    roles.add(result)
                elif c := ctx.guild.get_channel(result):
                    if isinstance(c, TextChannel):
                        channels.add(result)
                    elif isinstance(c, CategoryChannel):
                        categories.add(result)
                    else:
                        rejected.add(result)
                else:
                    rejected.add(result)

        embed = Embed(title=f"ToxBot Blacklist Settings", colour=0x87ceeb)
        embed.add_field(name="Users", value="\n".join(strset(users)) or "None")
        embed.add_field(name="Roles", value="\n".join(strset(roles)) or "None")
        embed.add_field(name="Channels", value="\n".join(strset(channels)) or "None")
        embed.add_field(name="Categories", value="\n".join(strset(categories)) or "None")
        embed.add_field(name="Rejected", value="\n".join(strset(rejected)) or "None")

        await response.delete()
        await reply.edit(content="Hold tight while I commit your settings...", embed=embed)

        config = copy(self.bot.db.default)

        config["prefix"] = prefix
        config["ignore"]["users"] = list(users)
        config["ignore"]["roles"] = list(roles)
        config["ignore"]["channels"] = list(channels)
        config["ignore"]["categories"] = list(categories)

        await self.bot.db.create_guild(ctx.guild.id, config)
        embed.description = f"Prefix: {prefix}\n\n**__Blacklist:__**"
        await reply.edit(content="Setup complete!", embed=embed)


def setup(bot: Bot):
    bot.add_cog(UI(bot))