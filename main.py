import os
import nextcord
import json
import datetime
import pytz
from nextcord.ext import commands

intents = nextcord.Intents.all()
intents.message_content = True

'''
This runs the config JSON file. This will not be included
on our GitHub Repostiory since it includes the token for our bot.

Once you run this file it will create the config.json file for you.
You will need to enter your bot token into the "" of the file.

All the code is open to anyone and can be used in your own projects :)
'''

# Checks if the JSON file exists.
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as x:
        configData = json.load(x)

# Creates the JSON file in the format for the developer.
else:
    # Template for the JSON file.
    configTemplate = {
                        "TOKEN": "", # INSERT TOKEN INSIDE "" (config.json)
                        "DATABASEPASSWORD": "" # INSERT DATABASE PASSWORD INSIDE "" (config.json)
                    }  

    # Creates the file and sets it to the same layout as our code.
    with open(os.getcwd() + "/config.json", "w+") as x:
        json.dump(configTemplate, x)

# Setting the prefix for the bot. "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Removes default help command so we can access our own custom one.
bot.remove_command('help')


# This will run once the bot is booted up.
@bot.event
async def on_ready():
    # Prints to console telling us that it is logged in.
    print(f'Logged in as {bot.user}\n')
    # Status for the bot.
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="/study"))

# Checking what version the bot is running on.
@bot.command()
# Checks if the user is a owner.
@commands.is_owner()
async def version(ctx):
    await ctx.send("Dino Bot is running on version **0.6.1 (Beta)**")

# Checking what time the bot is running on.
@bot.command()
@commands.is_owner()
async def time(ctx):
    await ctx.send(f"Dino Bot is running on **{(datetime.datetime.now(pytz.timezone('America/Los_Angeles')))}**")

# Loads a specific cog.
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f'commands.{extension}')
        await ctx.send("Loaded **" + extension + "** Cog.")
    except Exception:
        await ctx.send("Could not load **" + extension + "** Cog. (Check state of cog or spelling)")

# Unloads a specific cog.
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'commands.{extension}')
        await ctx.send("Unloaded **" + extension + "** Cog.")
    except Exception:
        await ctx.send("Could not unload **" + extension + "** Cog. (Check state of cog or spelling)")

# Reloads a specific cog.
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'commands.{extension}')
        await ctx.send("Reloaded **" + extension + "** Cog.")
    except Exception:
        await ctx.send("Could not reload **" + extension + "** Cog. (Check state of cog or spelling)")

# When the bot turns on this will load all the files in the helpers folder.
for filename in os.listdir('./helpers'):
    if filename.endswith('.py'):
        bot.load_extension(f'helpers.{filename[:-3]}')

# When the bot turns on this will load all the timer files in the database folder.
for filename in os.listdir('./database'):
    if filename.endswith('.py'):
        bot.load_extension(f'database.{filename[:-3]}')

# When the bot turns on this will load all the files in the commands folder.
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        # This will strip the last three characters from the files (.py)
        bot.load_extension(f'commands.{filename[:-3]}')

# When the bot turns on this will load all the study files in the commands/study folder.
for filename in os.listdir('./commands/study'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.study.{filename[:-3]}')

# When the bot turns on this will load all the timer files in the commands/timer folder.
for filename in os.listdir('./commands/timer'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.timer.{filename[:-3]}')


# Token from Secret Variable
bot.run(configData["TOKEN"])