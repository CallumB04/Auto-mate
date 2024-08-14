## Imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio, json
from bot import bot

## Creates a user account in the database for any new users
async def update_users(users, userid):
    if not userid in users:
        users[userid] = {}
        users[userid]["Experience"] = 0
        users[userid]["Level"] = 1

## Adds a given amount of experience points to the users total
async def add_experience(users, userid, exp):
    users[userid]["Experience"] += exp

## Checks if the user has enough experience points to level up
async def levelup(users, userid, channel):
    experience = users[userid]["Experience"]
    before = users[userid]["Level"]
    after = int(experience ** (1/4))

    ## If the user has enough for a level up
    if before < after:
        with open("./data/guilds.json", "r") as f:
            guilds = json.load(f)

            guildid = channel.guild.id
            levels_channel = guilds[str(guildid)]["channel_levels"]

            ## Checks if guilds has a set channel for level announcing. If not, the bot will default to the channel the user is messaging in.
            if levels_channel != "":
                channel = bot.get_channel(int(levels_channel))

            await channel.send(f"<@{userid}> has leveled up to level {after}!")
            users[userid]["Level"] = after

            ## Adding any guild roles set for certain levels
            try:
                roleid = guilds[str(channel.guild.id)]["role_levels"][str(after)] ## gets role id of the certain level
                
                ## fetches discord role and user objects from their respective ids
                if roleid != "":
                    role = channel.guild.get_role(int(roleid))
                    user = channel.guild.get_member(int(userid))

                    ## Gives the user the role once they hit the certain level
                    await user.add_roles(role)

            except Exception as e:
                if e == KeyError: ## level not in [5, 10, 20]
                    pass