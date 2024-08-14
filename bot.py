## Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio, json

intents = discord.Intents.all() ## discord requires you to enable intents for the bot to use certain features
bot = commands.Bot(command_prefix="?", intents=intents) ## Defines the bot object, uses a prefix of '?' for all commands

## Procedure that is ran when the Bot is initially activated!
@bot.event
async def on_ready():
    print("Bot is online!")

    ## Initialising the bots status from prior configuration if specified

    with open("./data/botinfo.json", "r") as f:
        info = json.load(f)

        ## extracts data from json into variables
        status = info["status_text"]
        mode = info["status_mode"]

        ## Calculates chosen status (default = Online)
        if mode in ["", "Online"]: status_mode = discord.Status.online
        elif mode == "Idle": status_mode = discord.Status.idle
        elif mode == "DND": status_mode = discord.Status.do_not_disturb

        ## Adds status text to bot (default = Server count)
        if status != "":
            game = discord.Game(status)
        else:
            guild_count = len(bot.guilds)
            brain_emoji = "\N{BRAIN}"
            game = discord.Game(f"{brain_emoji} Automating {guild_count} Servers!")

        await bot.change_presence(status=status_mode, activity=game)