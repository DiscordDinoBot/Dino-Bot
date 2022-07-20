import nextcord
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from .verification import Verification
        Buttons.verificationFile = Verification(bot)

class VerificationButtons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        from .verification import Verification
        Buttons.verificationFile = Verification(bot)

    async def setVerificationButtons(self):

        continueButton = Button(label="Continue Session", style=ButtonStyle.green)
        endButton = Button(label="End Session", style=ButtonStyle.red)

        # Button View for any paused sessions.
        VerificationButtons.verificationButtonView = View()
        VerificationButtons.verificationButtonView.add_item(continueButton)
        VerificationButtons.verificationButtonView.add_item(endButton)

        # Response functions.
        continueButton.callback = VerificationButtons.responseContinueButton
        endButton.callback = VerificationButtons.responseEndButton


    async def responseContinueButton(self):
        embed = nextcord.Embed(description=("Your session is **Continuing**."), colour=nextcord.Colour.from_rgb(57, 204, 86))
        await Buttons.verificationFile.verificationResponseMessage[self.user.id].edit(embed=embed, view=VerificationButtons.verificationButtonView)


    async def responseEndButton(self):
            # #Verification.finishState[self.user.id] = True
            # PomodoroInput.sessionActive[self.user.id] = False

            # # Trying to remove a selection menu.
            # try:
            #     await PomodoroInput.selectionMenuMessage[self.user.id].delete()

            # # No menu is active, therefore we pass it.
            # except nextcord.errors.NotFound:
            #     pass

            # # Trying to remove a pause message.
            # try:
            #     await PomodoroClock.pauseMessage[self.user.id].delete()

            #     # Since pause message is outside of the clock function we need to manually finish the session.
            #     await PomodoroClock.finishPomodoro(self, self.user, self.user.id)

            # # No pause message, therefore we pass it.
            # except (nextcord.errors.NotFound, KeyError):
            #     pass

            # embed = nextcord.Embed(description=(
            #     "Your session has **Stopped**. You can begin a new one."), colour=nextcord.Colour.from_rgb(209, 65, 65))
            # await PomodoroInput.removeMessage[self.user.id].edit(embed=embed, view=PomodoroInput.SessionButtons)

        pass

def setup(bot):
    bot.add_cog(Buttons(bot))