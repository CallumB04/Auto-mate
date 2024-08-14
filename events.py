## Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import levelling_system as lvl
import guilds as g
from bot import bot

## Procedure that is ran each time a user message is sent that the bot can see
@bot.event
async def on_message(message):

    ## ignores the message if the author is a discord bot
    if not message.author.bot:

        ## Checking server's banned word list
        with open("./data/guilds.json", "r") as f:
            guilds = json.load(f)

            ## iterating through each word in the message
            for word in message.content.split(" "):
                ## checking if word in banned list:
                if word.lower() in guilds[str(message.guild.id)]["word_list"]:
                    print("user said cheese")
                    await message.delete() ## deletes message
                    await message.channel.send(f"<@{message.author.id}>, Please do not use that word again!")

        ## Outputs users message in console
        print(f"{message.guild} ; {message.author.name} : {message.content}")

        ## Levelling system
        with open("./data/users.json", "r") as f:
            users = json.load(f) ## loads data into users as an object

        await lvl.update_users(users, str(message.author.id))
        await lvl.add_experience(users, str(message.author.id), 5)
        await lvl.levelup(users, str(message.author.id), message.channel)

        with open("./data/users.json", "w") as f:
            json.dump(users, f) ## overwrites data in file
            
        await bot.process_commands(message)  ## checks if the message contains is calling one of the commands

## Procedure that is ran each time a member joins a server the bot can see
@bot.event
async def on_member_join(member):

    ## Ignores the event if the member joining was a bot
    if not member.bot:
        print(f"{member.name}#{member.discriminator} has joined the server: {member.guild}")

        ## Welcoming member to the guild
        with open("./data/guilds.json") as f:
            guilds = json.load(f)
            
            channelid = guilds[str(member.guild.id)]["channel_welcomes"]

            if str(channelid) != "":
                ch = bot.get_channel(int(channelid))
                await ch.send(f"<@{member.id}> Welcome to the server!")

        ## Levelling system
        with open("./data/users.json", "r") as f:
            users = json.load(f) ## loads data into users as an object

        await lvl.update_users(users, str(member.id))

        with open("./data/users.json", "w") as f:
            json.dump(users, f) ## overwrites data in file

        ## Giving the members the auto assigned role (if exists)
        with open("./data/guilds.json", "r") as f:
            guilds = json.load(f)

            guildid = str(member.guild.id)

            roleid = guilds[guildid]["role_join"]
            if roleid != "":
                role = member.guild.get_role(int(roleid)) ## obtains the role object from the id

                try:
                    await member.add_roles(role) ## gives the member the allocated role
                except Exception as e:
                    if e == AttributeError:
                        pass


## Procedure that is ran each time the bot joins a new server
@bot.event 
async def on_guild_join(guild):
    print(f"Bot has joined the server: {guild.name}")

    ## Adding guild to database
    with open("./data/guilds.json", "r") as f:
        guilds = json.load(f)

        await g.update_guilds(guilds, str(guild.id)) ## adds guild to database

    with open("./data/guilds.json", "w") as f:
        json.dump(guilds, f)