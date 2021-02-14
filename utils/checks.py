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
