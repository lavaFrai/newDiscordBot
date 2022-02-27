import discord
import sqlite3
import time
from consts import *
from auxiliary import *

database = sqlite3.connect("sqlite.db")
cursor = database.cursor()


def main(client):
    def error(text, e=""):
        print("[ERROR]\t" + text + "\nError text: " + str(e) + "\n[Enter to finish]")
        input()
        exit(1)

    def info(text):
        print("[INFO]\t" + text)

    @client.event
    async def on_message(ctx):
        if debug:
            info(f"{time.asctime()} > "
                 f"Message from server \"{ctx.guild.name}\" "
                 f"in channel \"{ctx.channel.name}\" "
                 f"by \"{ctx.author.name}#{ctx.author.discriminator}\" "
                 f"content: \"{ctx.content}\"")

        _prefix = getServerPrefix(ctx)
        _message = str(ctx.content)
        _superuser = checkForSudo(ctx)

        if _message.startswith(_prefix) or _message.startswith(f"<@!{client.user.id}>"):
            # executing command
            _command = parseCommand(ctx)
            if debug:
                await ctx.reply(f"Debug: executing your command (Text: \"{_command}\") {'with' if _superuser else 'without'} superuser rules")

