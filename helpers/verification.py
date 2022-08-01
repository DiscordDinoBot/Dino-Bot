import nextcord
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands


class Verification(commands.Cog):
    def __init__(self, bot):
        Verification.bot = bot
        Verification.sessionActive = {}
        Verification.verificationResponseMessage = {}

    async def addUserVerification(userIdentity):
        Verification.sessionActive[userIdentity] = True

    async def removeUserVerification(userIdentity):
        try:
            del Verification.sessionActive[userIdentity]

        except (KeyError):
            pass

    async def removeMessage(self, userIdentity):
        embed = nextcord.Embed(description=(
            "Your session is **Continuing**."), colour=nextcord.Colour.from_rgb(57, 204, 86))
        await Verification.verificationResponseMessage[userIdentity].edit(view=None, embed=embed)

    async def getUserSessions(userIdentity):
        from commands.study.pomodoroClock import PomodoroClock
        from commands.study.pomodoroCustomInput import PomodoroCustomInput
        from commands.study.pomodoroInput import PomodoroInput
        from commands.timer.timer import Timer
        from commands.timer.timerInput import TimerInput

        userMessages = [PomodoroInput.selectionMenuMessage,
                        PomodoroClock.pomodoroMessage,
                        PomodoroCustomInput.customSelectionMenuMessage,
                        TimerInput.timerSelectionMenuMessage,
                        Timer.timerMessage,
                        Verification.verificationResponseMessage
                        ]

        userSessionStates = [PomodoroClock,
                             Timer
                             ]

        return userMessages, userSessionStates

    async def finishSessions(userSessionStates, userIdentity):
        for sessionState in userSessionStates:
            try:
                sessionState.finishState[userIdentity] = True

            except (nextcord.errors.NotFound, KeyError, AttributeError):
                pass

    async def removeMessage(userMessages, userIdentity):
        for message in userMessages:
            try:
                await message[userIdentity].delete()

            except (nextcord.errors.NotFound, KeyError):
                pass

    async def verificationResponse(self, user, userIdentity):
        try:
            await Verification.verificationResponseMessage[userIdentity].delete()

        except (KeyError, nextcord.errors.NotFound):
            pass

        await VerificationButtons.setVerificationButtons(self)
        embed = nextcord.Embed(description=(
            "You currently have an **active session.**"), colour=nextcord.Colour.from_rgb(209, 65, 65))
        Verification.verificationResponseMessage[userIdentity] = await user.send(view=VerificationButtons.verificationButtonView, embed=embed)

    async def verificationContinueResponse(self, userIdentity):
        embed = nextcord.Embed(description=(
            "Your session is **Continuing**."), colour=nextcord.Colour.from_rgb(57, 204, 86))
        await Verification.verificationResponseMessage[userIdentity].edit(view=None, embed=embed)

    async def verificationEndResponse(interaction):
        userMessages, userSessionStates = await Verification.getUserSessions(interaction.user.id)
        await Verification.finishSessions(userSessionStates, interaction.user.id)
        await Verification.removeMessage(userMessages, interaction.user.id)
        await Verification.removeUserVerification(interaction.user.id)


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
