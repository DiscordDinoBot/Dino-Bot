import nextcord
from nextcord.ext import commands


class Buttons(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    # INSERT ALL BUTTONS FOR THE BOT


def setup(bot):
    bot.add_cog(Buttons(bot))
