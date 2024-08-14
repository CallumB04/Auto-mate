## Imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
from bot import bot

## Creates a user account in the database for any new users
async def update_guilds(guilds, guildid):
    if not guildid in guilds:
        guilds[guildid] = {}
        guilds[guildid]["role_join"] = ""
        guilds[guildid]["role_levels"] = {5: "", 10: "", 20: ""}
        guilds[guildid]["channel_levels"] = ""
        guilds[guildid]["channel_welcomes"] = ""
        guilds[guildid]["word_list"] = []

## Bot command to set role users are given when joining server
@bot.command(name="setjoinrole")
async def set_join_role(ctx, role: discord.Role):

    ## Ensures the user is allowed to manage roles for the command
    if ctx.author.guild_permissions.manage_roles:

        ## Opening guilds database
        with open("./data/guilds.json", "r") as f:
            guilds = json.load(f)

            ## Adding automatic role to the database
            try:
                guilds[str(ctx.guild.id)]["role_join"] = str(role.id)
                await ctx.channel.send(f"<@{ctx.author.id}>, set the join role as <@&{role.id}>!")
                
            ## Exception for any predictable errors
            except Exception as e:
                if e == KeyError:
                    await ctx.channel.send(f"<@{ctx.author.id}>, failed to set join role. Please try again!")
                elif e == AttributeError:
                    await ctx.author.send("This command needs to be used inside of a guild!")

        with open("./data/guilds.json", "w") as f:
            json.dump(guilds, f)

    else:
        await ctx.channel.send(f"<@{ctx.author.id}>, you dont have the permissions to use this command!")

## Bot command to set role users are given when reaching a certain level
@bot.command(name="setlevelrole")
async def set_level_role(ctx, value, role: discord.Role):

    ## Ensures the user has role management permissions
    if ctx.author.guild_permissions.manage_roles:
        try:
            value = int(value) ## converts string into an integer

            ## Checks if level role exists in the bot
            if value in [5, 10, 20]:
                with open("./data/guilds.json", "r") as f:
                    guilds = json.load(f)

                    ## Adding level role to the database
                    try:
                        guilds[str(ctx.guild.id)]["role_levels"][str(value)] = str(role.id)
                        await ctx.channel.send(f"<@{ctx.author.id}>, set the Level {value} role as <@&{role.id}>!")
                        
                    ## Exception for any predictable errors
                    except Exception as e:
                        if e == KeyError:
                            await ctx.channel.send(f"<@{ctx.author.id}>, failed to set level role. Please try again!")
                        elif e == AttributeError:
                            await ctx.author.send("This command needs to be used inside of a guild!")

                with open("./data/guilds.json", "w") as f:
                    json.dump(guilds, f)
            else:
                await ctx.channel.send(f"<@{ctx.author.id}>, incorrect use of command. Please use ?setlevelrole <5/10/20>!")
        except Exception as e:
            ## if the user doesnt input an integer as the value
            if e == ValueError:
                await ctx.channel.send(f"<@{ctx.author.id}>, incorrect use of command. Please use ?setlevelrole <5/10/20>!")


    else:
        await ctx.channel.send(f"<@{ctx.author.id}>, you dont have the permissions to use this command!")

## Bot command to set channel for welcomes and level updates
@bot.command(name="setchannel")
async def set_channel(ctx, choice, channel: discord.TextChannel):

    ## Ensures only admins can use the command
    if ctx.author.guild_permissions.administrator:

        ## Channel for welcoming users
        if choice == "welcome":
            try:
                with open("./data/guilds.json", "r") as f:
                    guilds = json.load(f)

                    ## Sets the welcome channel in the database
                    guilds[str(ctx.guild.id)]["channel_welcomes"] = str(channel.id)
                    await ctx.channel.send(f"<@{ctx.author.id}>, the welcome channel has been set as <#{channel.id}>")

                with open("./data/guilds.json", "w") as f:
                    json.dump(guilds, f)

            ## Error handling
            except Exception as e:
                if e == ChannelNotFound:
                    await ctx.channel.send(f"<@{ctx.author.id}>, this channel does not exist. Please try again!")
                else:
                    pass

        ## Channel for announcing when a user levels up
        elif choice == "levels":
            try:
                with open("./data/guilds.json", "r") as f:
                    guilds = json.load(f)

                    ## Sets the levelling up channel in the database
                    guilds[str(ctx.guild.id)]["channel_levels"] = str(channel.id)
                    await ctx.channel.send(f"<@{ctx.author.id}>, the level up channel has been set as <#{channel.id}>")

                with open("./data/guilds.json", "w") as f:
                    json.dump(guilds, f)

            ## Error handling
            except Exception as e:
                if e == ChannelNotFound:
                    await ctx.channel.send(f"<@{ctx.author.id}>, this channel does not exist. Please try again!")
                else:
                    pass
        ## If no correct channel type is selected
        else:
            await ctx.channel.send(f"<@{ctx.author.id}>, you can not set a channel for this. Please try again <welcome/levels>!")
    else:
        await ctx.channel.send(f"<@{ctx.author.id}>, only admins can use this command!")

## Bot command to add a word to the banned word list
@bot.command(name="banword")
async def add_banned_word(ctx, word):

    ## Ensures user is allowed to use this command
    if ctx.author.guild_permissions.manage_messages:
        with open("./data/guilds.json", "r") as f:
            guilds = json.load(f)

            ## Adds word to the banned word list for that server
            guilds[str(ctx.guild.id)]["word_list"].append(word.lower())
            await ctx.channel.send(f"<@{ctx.author.id}>, the word has been added to the banned word list!")
        
        with open("./data/guilds.json", "w") as f:
            json.dump(guilds, f)

    else:
        await ctx.channel.send(f"<@{ctx.author.id}>, you dont have the permissions to use this command!")