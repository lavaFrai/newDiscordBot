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
                                                                           f"Author id: `{ctx.author.id}`"))

    @bot_module
    async def admin_add(ctx):
        if checkForSudo(ctx):
            admins = list(eval(str(databaseGet(f"SELECT admin FROM servers WHERE id=\"{ctx.guild.id}\"")[0][0])))
            new_admin = getFirstPing(ctx)
            if (new_admin is None) or (new_admin.id == ctx.guild.me.id):
                await ctx.reply(embed=Embed(title="Admin add", description=f"You need to enter the nickname of the new administrator"))
                return
            if new_admin.id in admins:
                await ctx.reply(embed=Embed(title="Admin add", description=f"{new_admin.name} is already an administrator"))
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
                await ctx.reply(embed=Embed(title="Admin remove", description=f"You need to enter the nickname of the new administrator"))
                return
            if new_admin.id not in admins:
                await ctx.reply(embed=Embed(title="Admin remove", description=f"{new_admin.name} isn't already an administrator"))
            else:
                admins.remove(new_admin.id)
                databaseSend(f"UPDATE servers SET admin=\"{str(admins)}\" WHERE id=\"{ctx.guild.id}\"")
                await ctx.reply(embed=Embed(title="Admin remove", description=f"{new_admin.name} no longer an administrator"))

    return commands
