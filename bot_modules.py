from auxiliary import *
from discord import Embed


def info(text):
    print("[INFO]\t" + text)


def main():
    commands = {}

    def bot_module(func):
        info(f"Registered module {func.__name__.lower()}")
        commands[func.__name__.lower()] = func

    @bot_module
    async def prefix(ctx):
        if len(getRealMessageText(ctx).strip()) > 0:
            if checkForSudo(ctx):
                databaseSend(f"UPDATE servers SET prefix=\"{prepareForDatabase(getRealMessageText(ctx).strip().split()[0])}\" WHERE id=\"{ctx.guild.id}\"")
                await ctx.reply(embed=Embed(title="Prefix change", description=f"New prefix is `{getServerPrefix(ctx)}`"))
            else:
                await ctx.reply("Sorry, not enough rights for this command")
        else:
            await ctx.reply(embed=Embed(title="Prefix", description=f"Current prefix is `{getServerPrefix(ctx)}`"))

    return commands
