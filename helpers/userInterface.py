import nextcord
from nextcord.ext import commands


class UserInterface(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    # INSERT ALL UI FOR THE BOT


def setup(bot):
    bot.add_cog(UserInterface(bot))