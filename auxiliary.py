import sqlite3
import discord
import time
from consts import *

database = sqlite3.connect("sqlite.db")
cursor = database.cursor()


def databaseGet(query):
    cursor.execute(query)
    return cursor.fetchall()


def prepareForDatabase(text: str):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def databaseSend(query):
    cursor.execute(query)
    database.commit()


def registrateNewServer(id):
    databaseSend(f"INSERT INTO servers VALUES (\"{id}\", \"{defaultPrefix}\", \"[]\")")
    pass


def checkForSudo(ctx):
    return ctx.author.id in eval(str(databaseGet(f"SELECT admin FROM servers WHERE id=\"{ctx.guild.id}\"")[0][0])) or \
           ctx.guild.owner_id == ctx.author.id


def getServerPrefix(ctx):
    _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
    if len(_prefix) > 0:
        _prefix = _prefix[0][0]
    else:
        registrateNewServer(ctx.guild.id)
        _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
        _prefix = _prefix[0][0]
    return _prefix


def parseCommand(ctx):
    message = str(ctx.content)
    lPtr = 0
    _prefix = getServerPrefix(ctx)

    # skipping prefix
    if message.startswith(_prefix):
        lPtr = len(_prefix)
    else:
        lPtr = message.find('>') + 1
    if lPtr >= len(message):
        return ""

    # skipping whitespace
    while (lPtr < len(message)) and (message[lPtr] in whitespaces):
        lPtr += 1

    # reading keyword
    rPtr = lPtr
    while (rPtr < len(message)) and (message[rPtr] not in whitespaces):
        rPtr += 1

    return message[lPtr:rPtr]


def getRealMessageText(ctx):
    message = str(ctx.content)
    lPtr = 0
    _prefix = getServerPrefix(ctx)

    # skipping prefix
    if message.startswith(_prefix):
        lPtr = len(_prefix)
    else:
        lPtr = message.find('>') + 1
    if lPtr >= len(message):
        return ""

    # skipping whitespace
    while (lPtr < len(message)) and (message[lPtr] in whitespaces):
        lPtr += 1

    # reading keyword
    rPtr = lPtr
    while (rPtr < len(message)) and (message[rPtr] not in whitespaces):
        rPtr += 1

    # skipping whitespace
    while (rPtr < len(message)) and (message[rPtr] in whitespaces):
        rPtr += 1

    return message[rPtr:]
