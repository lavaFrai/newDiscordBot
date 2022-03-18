import discord
import sqlite3
import time
from consts import *
from auxiliary import *

global modules
modules = {}


def error(text, e=""):
    print("[ERROR]\t" + text + "\nError text: " + str(e) + "\n[Enter to finish]")
    input()
    exit(1)


def info(text):
    print("[INFO]\t" + text)


def registrateModulesFile(path):
    global modules
    try:
        modules = mergeDict(__import__(path).main(), modules)
    except ImportError as e:
        error(f"Can not import module '{path}' may be try without .py at end of name&", e)


database = sqlite3.connect("sqlite.db")
cursor = database.cursor()
text_commands = __import__("text_commands").main()

# Extension modules registration
registrateModulesFile("bot_modules")
# for example:
registrateModulesFile("example_modules_file")


def main(client):
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
        _realtext = getRealMessageText(ctx)

        if _message.startswith(_prefix) or _message.startswith(f"<@!{client.user.id}>"):
            # executing command
            _command = parseCommand(ctx).lower()
            if debug:
                await ctx.reply(
                    f"Debug: executing your command (Text: \"{_command}\") {'with' if _superuser else 'without'} superuser rules")
            if _command in text_commands:
                await ctx.reply(text_commands[_command](ctx))
            if _command in modules:
                await modules[_command](ctx)
