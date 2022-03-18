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

    # Example module
    @bot_module
    async def test_module(ctx: discord.Message):
        await ctx.reply("ku, pidor")

    # Your modules

    return commands


# !!! Don't forget to register in handler.py
