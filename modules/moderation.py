import discord
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
    async def kick(ctx: discord.Message):
        if checkForSudo(ctx):
            try:
                await getFirstPing(ctx).kick()
                await ctx.reply(embed=Embed(title="Kick member", description="Ok, he is kicked 👍"))
            except discord.errors.Forbidden:
                await ctx.reply(embed=Embed(title="Kick member", description="Woops! It looks like I don't have enough rights to do this"))

    @bot_module
    async def ban(ctx: discord.Message):
        if checkForSudo(ctx):
            try:
                await getFirstPing(ctx).ban()
                await ctx.reply(embed=Embed(title="Ban member", description="Ok, he is banned 👍"))
            except discord.errors.Forbidden:
                await ctx.reply(embed=Embed(title="Ban member", description="Woops! It looks like I don't have enough rights to do this"))

    @bot_module
    async def warn(ctx: discord.Message):
        if checkForSudo(ctx):
            try:
                warnMember(getFirstPing(ctx))
                await ctx.reply(embed=Embed(title="Warn member", description="Ok, he is warned"))
            except discord.errors.Forbidden:
                await ctx.reply(embed=Embed(title="Warn member", description="Woops! It looks like I don't have enough rights to do this"))

    @bot_module
    async def warns(ctx: discord.Message):
        try:
            request = getMemberWarns(getFirstPing(ctx))
            if len(request) > 0:
                await ctx.reply(embed=Embed(title=f"Warnings of {getFirstPing(ctx).name}", description=f"{getFirstPing(ctx).name} has {len(request)} warnings```\n" +
                                                                                                       '\n'.join(list(map(lambda x: f"Warning of {getFirstPing(ctx)} id: {str(x[4])}", request))) +
                                                                                                       f" ```\nto remove warning type:\n{getServerPrefix(ctx)}unwarn <@{getFirstPing(ctx).id}> <warn id>"))
            else:
                await ctx.reply(embed=Embed(title=f"Warnings of {getFirstPing(ctx).name}", description=f"{getFirstPing(ctx).name} has not warnings"))
        except discord.errors.Forbidden:
            await ctx.reply(embed=Embed(title=f"Warnings of {getFirstPing(ctx).name}",
                                        description="Woops! It looks like I don't have enough rights to do this"))

    @bot_module
    async def unwarn(ctx: discord.Message):
        if checkForSudo(ctx):
            if dewarnMember(getFirstPing(ctx), int(str(ctx.content).strip().split()[-1])):
                await ctx.reply(embed=Embed(title="Warn member", description="Ok, warning removed"))
            else:
                await ctx.reply(embed=Embed(title="Warn member", description="He have not this warn"))

    return commands
