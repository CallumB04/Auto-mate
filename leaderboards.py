## Imports 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
from bot import bot

## Bot command to display leaderboard of users XP
@bot.command()
async def leaderboard(ctx):
    with open("./data/users.json", "r") as f:
        users = json.load(f)

        embed = discord.Embed(title = "Leaderboards", color = discord.Colour.purple())

        users_xp = {} ## dict for all users

        ## users stored as array [xp, level] ------ users_xp[user][0] = xp of user
        for user in users:
            users_xp[user] = []
            users_xp[user].append(users[user]["Experience"])
            users_xp[user].append(users[user]["Level"])

        ## Sorts the users by their Experience Points
        sorted_users = dict(sorted(users_xp.items(), key=lambda item: item[1][0], reverse=True))

        leaderboard_text_array = []

        ## Iterates through the top 10 users, ordered by XP
        for index, user in enumerate(sorted_users):
            if index < 10:
                user_obj = bot.get_user(int(user)) ## gets the user object from the id
                username = user_obj.name + "#" + user_obj.discriminator

                ## Adds the user to an array that will be converted into a string to add to the embed
                leaderboard_text_array.append(f"`{index+1})` {username.capitalize()} -> {sorted_users[user][0]} XP ( Level: {sorted_users[user][1]} )")
            else: break

        ## Creates the text to be used for the leaderboard embed
        leaderboard_text = "\n".join(leaderboard_text_array)

        ## Adds the leaderboard text to the embed
        embed.add_field(name = "Top 10 users (XP) ", value = leaderboard_text, inline=False)

        await ctx.channel.send(embed=embed) ## outputs embed to the channel 