import nextcord
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands
from commands.study.pomodoroClock import PomodoroClock


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Verification.sessionActive = {}
        Verification.verificationResponseMessage = {}

        Verification.pomodoroClockFile = PomodoroClock(bot)

    async def addUserVerification(userIdentity):
        Verification.sessionActive[userIdentity] = True

    async def removeUserVerification(userIdentity):
        del Verification.sessionActive[userIdentity]

    async def removeMessage(self, user, userIdentity):

        from commands.study.pomodoroInput import PomodoroInput

        # Trying to remove a selection menu.
        try:
            await PomodoroInput.selectionMenuMessage[userIdentity].delete()

        # No menu is active, therefore we pass it.
        except nextcord.errors.NotFound:
            pass

        # Trying to remove a pause message.
        try:
            await PomodoroClock.pauseMessage[userIdentity].delete()

            # Since pause message is outside of the clock function we need to manually finish the session.
            await PomodoroClock.finishPomodoro(self, user, userIdentity)

        # No pause message, therefore we pass it.
        except (nextcord.errors.NotFound, KeyError):
            pass

    async def verificationResponse(self, user, userIdentity):
        await VerificationButtons.setVerificationButtons(self)
        embed = nextcord.Embed(description=(
            "You currently have an **active session.**"), colour=nextcord.Colour.from_rgb(209, 65, 65))
        Verification.verificationResponseMessage[userIdentity] = await user.send(view=VerificationButtons.verificationButtonView, embed=embed)

    async def verificationContinueResponse(self, userIdentity):
        embed = nextcord.Embed(description=(
            "Your session is **Continuing**."), colour=nextcord.Colour.from_rgb(57, 204, 86))
        await Verification.verificationResponseMessage[userIdentity].edit(view=None, embed=embed)

    async def verificationEndResponse(self):

        #RUN FINISH POMODORO FUNCTION

        PomodoroClock.finishState[self.user.id] = True
        await Verification.removeUserVerification(self.user.id)
        await Verification.removeMessage(self, self.user, self.user.id)

        embed = nextcord.Embed(description=(
            "Your session has **Stopped**. You can begin a new one."), colour=nextcord.Colour.from_rgb(209, 65, 65))
        await Verification.verificationResponseMessage[self.user.id].edit(view=None, embed=embed)


class VerificationButtons(commands.Cog):

    async def setVerificationButtons(self):
        continueButton = Button(label="Continue Session",
                                style=ButtonStyle.green)
        endButton = Button(label="End Session", style=ButtonStyle.red)

        # Button View for any paused sessions.
        VerificationButtons.verificationButtonView = View()
        VerificationButtons.verificationButtonView.add_item(continueButton)
        VerificationButtons.verificationButtonView.add_item(endButton)

        # Response functions.
        continueButton.callback = VerificationButtons.responseContinueButton
        endButton.callback = VerificationButtons.responseEndButton

    async def responseContinueButton(self):
        await Verification.verificationContinueResponse(self.user, self.user.id)

    async def responseEndButton(self):
        await Verification.verificationEndResponse(self)


def setup(bot):
    bot.add_cog(Verification(bot))
