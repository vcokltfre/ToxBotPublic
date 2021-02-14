from discord.ext.commands import check, Context

def noadmin():
    async def predicate(ctx: Context):
        if ctx.bot.ENV == "dev":
            return True
        if ctx.me.guild_permissions.administrator:
            print(ctx.me.guild_permissions)
            await ctx.reply("I can't execute commands while I have the administrator permission.")
            return False
        return True

    return check(predicate)

def has_setup():
    async def predicate(ctx: Context):
        c = await ctx.bot.db.get_guild_config(ctx.guild.id)

        if not c:
            await ctx.reply(f"You need to set up your guild before you can run config commands. Use `{ctx.prefix}setup` to start.")
            return False

        return True

    return check(predicate)
