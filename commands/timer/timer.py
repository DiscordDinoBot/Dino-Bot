import nextcord
from datetime import date
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands
from asyncio import sleep
from helpers.userInterface import UserInterface
from helpers.verification import Verification


class Timer(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

        Timer.timerFinishState = {}
        Timer.timerPauseState = {}
        Timer.timeStudied = {}
        Timer.pauseMessage = {}
        Timer.timeRemaining = {}

    async def timerSet(self, userIdentity):
        Timer.timeStudied[userIdentity] = 0
        await TimerButtons.setTimerButtons(self)

    async def timerClock(self, user, userIdentity, timeSeconds):
        displayDescription = await UserInterface.getDisplayDescription(timeSeconds)
        embed = nextcord.Embed(title=(f"Timer"), description=(
            displayDescription), colour=nextcord.Colour.from_rgb(196, 138, 51))

        displayMessage = await user.send(view=TimerButtons.timerButtonView, embed=embed)

        initialSeconds = timeSeconds

        Timer.timerFinishState[userIdentity] = False
        Timer.timerPauseState[userIdentity] = False

        while (timeSeconds > 0) and (Timer.timerFinishState[userIdentity] == False) and (Timer.timerPauseState[userIdentity] == False):
            await sleep(1)
            timeSeconds -= 1

            if ((timeSeconds % 60) == 0):
                displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

                embed = nextcord.Embed(title=(f"Timer"), description=(
                    displayDescription), colour=nextcord.Colour.from_rgb(196, 138, 51))
                await displayMessage.edit(view=TimerButtons.timerButtonView, embed=embed)

        await displayMessage.delete()

        timeStudied = initialSeconds - timeSeconds
        Timer.timeStudied[userIdentity] += timeStudied
        Timer.timeRemaining[userIdentity] = timeSeconds

        if (Timer.timerFinishState[userIdentity] == True) or (timeSeconds <= 0):
            await Timer.timerFinish(user, userIdentity)

        else:
            await Timer.timerPause(user, userIdentity)

    async def timerPause(user, userIdentity):
        embed = nextcord.Embed(title=(f"Timer"), description=(
            "Your timer is paused."), colour=nextcord.Colour.from_rgb(237, 146, 71))
        Timer.pauseMessage[userIdentity] = await user.send(view=TimerButtons.timerPausedView, embed=embed)

    async def timerFinish(user, userIdentity):
        timeSeconds = Timer.timeStudied[userIdentity]
        finishDisplayDescription = await UserInterface.getFinishDisplayDescription(timeSeconds)
        studyDate = date.today()

        embed = nextcord.Embed(title=(f"Finished Session ({studyDate})"), description=(
            finishDisplayDescription), colour=nextcord.Colour.from_rgb(74, 189, 100))

        await user.send(embed=embed)

        await Verification.removeUserVerification(userIdentity)


class TimerButtons():
    def __init__(self, bot):
        self.bot = bot

    async def setTimerButtons(self):
        finishButton = Button(label="Finish",
                              style=ButtonStyle.green)
        pauseButton = Button(label="Pause", style=ButtonStyle.red)
        resumeButton = Button(label="Resume", style=ButtonStyle.green)

        TimerButtons.timerButtonView = View()
        TimerButtons.timerButtonView.add_item(finishButton)
        TimerButtons.timerButtonView.add_item(pauseButton)

        TimerButtons.timerPausedView = View()
        TimerButtons.timerPausedView.add_item(resumeButton)

        # Response functions.
        finishButton.callback = TimerButtons.responseFinishButton
        pauseButton.callback = TimerButtons.responsePauseButton
        resumeButton.callback = TimerButtons.responseResumeButton

    async def responseFinishButton(interaction):
        Timer.timerFinishState[interaction.user.id] = True

    async def responsePauseButton(interaction):
        Timer.timerPauseState[interaction.user.id] = True

    async def responseResumeButton(interaction):
        await Timer.pauseMessage[interaction.user.id].delete()
        timeSeconds = Timer.timeRemaining[interaction.user.id]
        await Timer.timerClock(interaction, interaction.user, interaction.user.id, timeSeconds)


# Setup function.
def setup(bot):
    bot.add_cog(Timer(bot))
