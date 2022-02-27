import discord

global client
client = discord.Client()

from handler import main


def error(text, e=""):
    print("[ERROR]\t" + text + "\nError text: " + str(e) + "\n[Enter to finish]")
    input()
    exit(1)


def info(text):
    print("[INFO]\t" + text)


@client.event
async def on_ready():
    info("Login successfully")


try:
    config_file = open("settings.env", "r")
    config = eval(config_file.read())
    main(client)
    info("Server starting with settings: " + str(config))
except BaseException as e:
    error("Can not open or read and parse settings file", e)
    exit(-1)

try:
    client.run(config["token"])
    info("Bot server finished")
except BaseException as e:
    error("Can not initialize bot", e)

error("program finished")
