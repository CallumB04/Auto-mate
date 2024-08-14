## === Auto-Mate ~ A Discord server moderation bot ~ Written in Python 3.10.0 ===

## Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
from bot import bot
from events import *
from guilds import *
from levelling_system import *
from leaderboards import *
from setup import *

## Bot command - deletes a specified amount of messages from the certain channel
@bot.command()
async def clear(ctx, amount: int):

    if amount < 1:
        await ctx.channel.send(f"<@{ctx.message.author.id}>, please input an amount greater than 0")
        return

    ## ensures the user should be allowed to use the command
    if ctx.message.author.guild_permissions.manage_messages:

        ## Deletes messages and outputs to the user
        await ctx.channel.purge(limit=amount, before=ctx.message) 
        await ctx.channel.send(f"Deleted {amount} Messages from chat! <@{ctx.message.author.id}>")

    ## if the user doesnt have message management
    else:
        await ctx.channel.send(f"You do not have the permissions to use that command! <@{ctx.message.author.id}>")

## Bot command - purges the whole entire server of all channels, roles and emojis
## Can only be performed by the owner of the server for security reasons
@bot.command()
async def destruct(ctx):
    ## ensures message author is the server owner
    if ctx.message.author.id == ctx.message.guild.owner_id:

        def check(m):
            return m.author.id == ctx.message.author.id and m.channel == ctx.message.channel

        ## Giving final chance to the owner
        await ctx.channel.send(f"Are you sure you want to remove everything from this server? [Y/N] <@{ctx.message.author.id}>")
        msg = await bot.wait_for("message", check=check)

        if msg.content.lower() == "y":

            ## Removing Text and Voice channels
            for channel in ctx.message.guild.channels:      
                try: await channel.delete(reason="Purge!")
                except: pass

            ## Removing roles
            for role in ctx.message.guild.roles:            
                try: await role.delete(reason="Purge!")
                except: pass
                
            ## Removing emojis
            for emoji in ctx.message.guild.emojis:          
                try: await emoji.delete(reason="Purge!")
                except: pass
            
            ## Creating temporary text channel after destruction is complete
            purge_channel = await ctx.message.guild.create_text_channel("new-beginnings")
            await purge_channel.send("Destruction complete!")
            await purge_channel.send("https://tenor.com/view/sponge-bob-square-pants-animation-cartoon-comedy-complete-gif-3473690")

        ## Destruction being cancelled
        elif msg.content.lower() == "n":
            await ctx.channel.send(f"Destruction cancelled! <@{ctx.message.author.id}>")
        else:
            await ctx.channel.send(f"Incorrect input, command was cancelled! <@{ctx.message.author.id}>")
    else:
        await ctx.channel.send(f"Only the owner can use this command! <@{ctx.message.author.id}>")

## Runs the tkinter setup window
setup()

## Obtains the bot's secret token from the json file
## Prevents the token being in the main code file, allowing for the code to be open source
with open("./data/botinfo.json", "r") as f:
    bot_info = json.load(f)
    TOKEN = bot_info["token"]

## Activates the bot, using its unique token
bot.run(TOKEN)