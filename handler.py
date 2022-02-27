import discord
import sqlite3
import time
from consts import *

database = sqlite3.connect("sqlite.db")
cursor = database.cursor()


def databaseGet(query):
    cursor.execute(query)
    return cursor.fetchall()


def databaseSend(query):
    cursor.execute(query)
    database.commit()


def registrateNewServer(id):
    databaseSend(f"INSERT INTO servers VALUES (\"{id}\", \"{defaultPrefix}\", \"[]\")")
    pass


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
        _message = str(ctx.content)
        _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
        if len(_prefix) > 0:
            _prefix = _prefix[0][0]
        else:
            registrateNewServer(ctx.guild.id)
            _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
            _prefix = _prefix[0][0]
        if _message.startswith(_prefix) or client.user == ctx.mentions[0]:
            info("Parsing command...")
            # executing command
