from nextcord.ext import commands


class Verification(commands.Cog):
    def __init__(self, bot):
        Verification.bot = bot

        # Creating the dictionaries that holds which users are active.
        Verification.sessionActive = {}

    # Adding the user to the session active dictionary.
    async def addUserVerification(userIdentity):
        Verification.sessionActive[userIdentity] = True

    # Removing the user from the session active dictionary.
    async def removeUserVerification(userIdentity):
        try:
            del Verification.sessionActive[userIdentity]

        except (KeyError):
            pass


def setup(bot):
    bot.add_cog(Verification(bot))
