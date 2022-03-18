import sqlite3
import discord
import time
from consts import *

database = sqlite3.connect("sqlite.db")
cursor = database.cursor()


def mergeDict(dict1, dict2):
    for k, v in dict2.items():
        if dict1.get(k):
            dict1[k] = [dict1[k], v]
        else:
            dict1[k] = v
    return dict1


def databaseGet(query):
    cursor.execute(query)
    return cursor.fetchall()


def prepareForDatabase(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"')


def databaseSend(query):
    cursor.execute(query)
    database.commit()


def registrateNewServer(id):
    databaseSend(f"INSERT INTO servers VALUES (\"{id}\", \"{defaultPrefix}\", \"[]\")")
    pass


def checkForSudo(ctx) -> bool:
    return ctx.author.id in eval(str(databaseGet(f"SELECT admin FROM servers WHERE id=\"{ctx.guild.id}\"")[0][0])) or \
           ctx.guild.owner_id == ctx.author.id


def getServerPrefix(ctx) -> str:
    _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
    if len(_prefix) > 0:
        _prefix = _prefix[0][0]
    else:
        registrateNewServer(ctx.guild.id)
        _prefix = databaseGet(f"SELECT prefix FROM servers WHERE id=\"{ctx.guild.id}\"")
        _prefix = _prefix[0][0]
    return _prefix


def parseCommand(ctx) -> str:
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


def getRealMessageText(ctx) -> str:
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


def getFirstPing(ctx) -> discord.Member:
    message = str(ctx.content)
    _prefix = getServerPrefix(ctx)

    if message.startswith(_prefix):
        return ctx.mentions[0] if len(ctx.mentions) > 0 else None
    else:
        return ctx.mentions[1] if len(ctx.mentions) > 0 else None
