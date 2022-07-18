import nextcord
from nextcord.ext import commands


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Verification.sessionActive = {}

    def addUserVerification(userIdentity):
        Verification.sessionActive[userIdentity] = True

    def removeUserVerification(userIdentity):
        del Verification.sessionActive[userIdentity]

    # INSERT ALL VERIFICATION ASPECTS TO THE BOT


# Setup function.
def setup(bot):
    bot.add_cog(Verification(bot))
