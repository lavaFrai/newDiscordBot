import queue
import subprocess
from auxiliary import *
from discord import Embed
import time
import threading
import sys


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
                databaseSend(
                    f"UPDATE servers SET prefix=\"{prepareForDatabase(getRealMessageText(ctx).strip().split()[0])}\" WHERE id=\"{ctx.guild.id}\"")
                await ctx.reply(
                    embed=Embed(title="Prefix change", description=f"New prefix is `{getServerPrefix(ctx)}`"))
            else:
                await ctx.reply("Sorry, not enough rights for this command")
        else:
            await ctx.reply(embed=Embed(title="Prefix", description=f"Current prefix is `{getServerPrefix(ctx)}`"))

    @bot_module
    async def debuginfo(ctx):
        await ctx.reply(embed=Embed(title="Debug information", description=f"Server id: `{ctx.guild.id}` \n"
                                                                           f"Channel id: `{ctx.channel.id}` \n"
                                                                           f"Author id: `{ctx.author.id}`"
                                                                           f"Superuser rules: `{checkForSudo(ctx)}` \n"
                                                                           f"Message real content: `{getRealMessageText(ctx)}` \n"
                                                                           f"Server prefix: `{getServerPrefix(ctx)}` \n"))

    @bot_module
    async def admin_add(ctx):
        if checkForSudo(ctx):
            admins = list(eval(str(databaseGet(f"SELECT admin FROM servers WHERE id=\"{ctx.guild.id}\"")[0][0])))
            new_admin = getFirstPing(ctx)
            if (new_admin is None) or (new_admin.id == ctx.guild.me.id):
                await ctx.reply(embed=Embed(title="Admin add",
                                            description=f"You need to enter the nickname of the new administrator"))
                return
            if new_admin.id in admins:
                await ctx.reply(
                    embed=Embed(title="Admin add", description=f"{new_admin.name} is already an administrator"))
            else:
                admins.append(new_admin.id)
                databaseSend(f"UPDATE servers SET admin=\"{str(admins)}\" WHERE id=\"{ctx.guild.id}\"")
                await ctx.reply(embed=Embed(title="Admin add", description=f"{new_admin.name} is new administrator"))

    @bot_module
    async def admin_remove(ctx):
        if checkForSudo(ctx):
            admins = list(eval(str(databaseGet(f"SELECT admin FROM servers WHERE id=\"{ctx.guild.id}\"")[0][0])))
            new_admin = getFirstPing(ctx)
            if (new_admin is None) or (new_admin.id == ctx.guild.me.id):
                await ctx.reply(embed=Embed(title="Admin remove",
                                            description=f"You need to enter the nickname of the new administrator"))
                return
            if new_admin.id not in admins:
                await ctx.reply(
                    embed=Embed(title="Admin remove", description=f"{new_admin.name} isn't already an administrator"))
            else:
                admins.remove(new_admin.id)
                databaseSend(f"UPDATE servers SET admin=\"{str(admins)}\" WHERE id=\"{ctx.guild.id}\"")
                await ctx.reply(
                    embed=Embed(title="Admin remove", description=f"{new_admin.name} no longer an administrator"))

    @bot_module
    async def calc(ctx):
        expression = getRealMessageText(ctx)
        if expression.find("__") != -1:
            await ctx.reply(embed=Embed(title="Execution result of expression", description=f"Error: \n"
                                                                                            f" `Security error: Not a safe expression ` \n"))
            return
        result = None

        # def executor(exp: str, result: queue.Queue) -> str:
        #     result.put(eval(str(exp), {'__builtins__': allowed_functions}))

        # res = queue.Queue()
        # thread = threading.Thread(target=executor, args=[expression, res])
        # thread.daemon = True
        # thread.start()
        # print("Running...", expression)
        # thread.join(5)
        # print("Finish")

        # if thread.is_alive() or res.empty():
        #     # thread.terminate()
        #     await ctx.reply(embed=Embed(title="Execution result of expression", description=f"Error: \n"
        #                                                                                     f" `Security error: Timed out ` \n"))
        #     return
        # result = res.get()

        # result = eval(str(expression), {'__builtins__': allowed_functions})
        executorText = ["python", "calculator.py"]
        executor = subprocess.Popen(executorText,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        try:
            outs, errs = executor.communicate(input=bytes(str(expression), encoding='utf8'), timeout=5)
        except subprocess.TimeoutExpired as e:
            executor.kill()
            outs, errs = executor.communicate()
            print("Timeout")
            outs = b"ERROR\0calculation timeout"
        # print(errs)
        status = outs[:outs.decode(encoding='utf8').index('\0')]
        out = outs[outs.decode(encoding='utf8').index('\0') + 1:]
        # print(status, out)
        if status == 'OK':
            await ctx.reply(embed=Embed(title="Execution result of expression", description=f"Expression: \n"
                                                                                            f"```python\n{expression} ``` \n"
                                                                                            f"Result: \n"
                                                                                            f"```python\n{out.decode(encoding='utf8')} ``` \n"))
        else:
            await ctx.reply(embed=Embed(title="Execution finished with error", description=f"Expression: \n"
                                                                                           f"```python\n{expression} ``` \n"
                                                                                           f"Error: \n"
                                                                                           f"```python\n{out.decode(encoding='utf8')} ``` \n"))

        print(expression, result)

    return commands
