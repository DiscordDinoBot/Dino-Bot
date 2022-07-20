import nextcord, asyncio
from nextcord.ext import commands
from .buttons import VerificationButtons

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Verification.sessionActive = {}
        Verification.verificationResponseMessage = {}

    async def addUserVerification(userIdentity):
        Verification.sessionActive[userIdentity] = True

    async def removeUserVerification(userIdentity):
        del Verification.sessionActive[userIdentity]

    # INSERT ALL VERIFICATION ASPECTS TO THE BOT

    async def verificationResponse(self, user, userIdentity):
        await VerificationButtons.setVerificationButtons(self)
        embed = nextcord.Embed(description=(
            "You currently have an **active session.**"), colour=nextcord.Colour.from_rgb(209, 65, 65))
        Verification.verificationResponseMessage[userIdentity] = await user.send(view=VerificationButtons.verificationButtonView, embed=embed)
     
def setup(bot):
    bot.add_cog(Verification(bot))