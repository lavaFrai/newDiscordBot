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
        info(f"{time.asctime()} > "
             f"Message from server \"{ctx.guild.name}\" "
             f"in channel \"{ctx.channel.name}\" "
             f"by \"{ctx.author.name}#{ctx.author.discriminator}\" "
             f"content: \"{ctx.content}\"")

        _prefix = getServerPrefix(ctx)
        _message = str(ctx.content)
        _superuser = checkForSudo(ctx)

        if _message.startswith(_prefix) or (client.user == ctx.mentions[0] if len(ctx.mentions > 0) else False):
            info(f"Parsing command {'SUDO' if _superuser else ''}...")
            # executing command
