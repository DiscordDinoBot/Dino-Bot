import os, nextcord, json

from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

'''
This runs the config JSON file. This will not be included
on our GitHub Repostiory since it includes the token for our bot.

Once you run this file it will create the config.json file for you.
You will need to enter your bot token into the "" of the file.
'''

#Checks if the JSON file exists.
if os.path.exists(os.getcwd() + "/config.json"):
  with open("./config.json") as x:
    configData = json.load(x)

#Creates the JSON file in the format for the developer.
else:
  #Template for the JSON file.
  configTemplate = {"TOKEN": ""} #INSERT TOKEN INSIDE ""
  
  #Creates the file and sets it to the same layout as our code.
  with open(os.getcwd() + "/config.json", "w+") as x:
    json.dump(configTemplate, x)

#Setting the prefix for the bot. "!"
bot = commands.Bot(command_prefix = "!", intents=intents)

#Removes default help command so we can access our own custom one.
bot.remove_command('help')

#This will run once the bot is booted up.
@bot.event
async def on_ready():
  #Prints to console telling us that it is logged in.
  print(f'Logged in as {bot.user}\n')
  #Status for the bot.
  await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="!study"))


#Loads a specific cog.
@bot.command()
#Checks if the user is a owner.
@commands.is_owner()
async def load(ctx, extension):
  try:
    bot.load_extension(f'commands.{extension}')
    await ctx.send("Loaded **" + extension + "** Cog.")
  except Exception:
    await ctx.send("Could not load **" + extension + "** Cog. (Check state of cog or spelling)")


#Unloads a specific cog.
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
  try:
    bot.unload_extension(f'commands.{extension}')
    await ctx.send("Unloaded **" + extension + "** Cog.")
  except Exception:
    await ctx.send("Could not unload **" + extension + "** Cog. (Check state of cog or spelling)")


#Reloads a specific cog.
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
  try:
    bot.reload_extension(f'commands.{extension}')
    await ctx.send("Reloaded **" + extension + "** Cog.")
  except Exception:
    await ctx.send("Could not reload **" + extension + "** Cog. (Check state of cog or spelling)")


#When the bot turns on this will load all the files in the commands folder.
for filename in os.listdir('./commands'):
  if filename.endswith('.py'):
    #This will strip the last three characters from the files (.py)
    bot.load_extension(f'commands.{filename[:-3]}')

#When the bot turns on this will load all the study files in the commands/study folder.
for filename in os.listdir('./commands/study'):
  if filename.endswith('.py'):
    bot.load_extension(f'commands.study.{filename[:-3]}') 

#Token from Secret Variable
bot.run(configData["TOKEN"])