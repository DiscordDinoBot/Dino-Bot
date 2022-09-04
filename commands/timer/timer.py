import nextcord
from datetime import date
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands
from asyncio import sleep
from helpers.userInterface import UserInterface
from database.database import Database


class Timer(commands.Cog):
    def __init__(self, bot):

        Timer.bot = bot

        # Dictionaries used to contain the variables used in the timer.
        Timer.timerMessage = {}
        Timer.finishState = {}
        Timer.pauseState = {}
        Timer.timeStudied = {}
        Timer.timeRemaining = {}

    async def timerSet(self, userIdentity):
        await TimerButtons.setTimerButtons(self)

        Timer.timeStudied[userIdentity] = 0
        Timer.finishState[userIdentity] = False
        Timer.pauseState[userIdentity] = False

    async def timerClock(self, user, userIdentity, timeSeconds):
        displayDescription = await UserInterface.getDisplayDescription(timeSeconds)
        # Setting up the embed for the timer message.
        embed = nextcord.Embed(title=(f"Timer"), description=(
            displayDescription), colour=nextcord.Colour.from_rgb(196, 138, 51))

        # Assigning the timer message to a variable so we can delete it when the timer is finished or paused.
        Timer.timerMessage[userIdentity] = await user.send(view=TimerButtons.timerButtonView, embed=embed)

        # Keeping track of the initalTime so we can see how much time elasped.
        initialSeconds = timeSeconds

        while (timeSeconds > 0) and (Timer.finishState[userIdentity] == False) and (Timer.pauseState[userIdentity] == False):
            await sleep(1)

            # Checks if a minute has passed. If this is true we must update the display of the timer.
            if ((timeSeconds % 60) == 0):
                displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

                embed = nextcord.Embed(title=(f"Timer"), description=(
                    displayDescription), colour=nextcord.Colour.from_rgb(196, 138, 51))
                await Timer.timerMessage[userIdentity].edit(view=TimerButtons.timerButtonView, embed=embed)

            timeSeconds -= 1

        try:
            # Deletes the timer message.
            await Timer.timerMessage[userIdentity].delete()

        except (nextcord.errors.NotFound):
            pass

        # Calculates how much time has passed and adds it to variables.
        timeStudied = initialSeconds - timeSeconds
        Timer.timeStudied[userIdentity] += timeStudied
        Timer.timeRemaining[userIdentity] = timeSeconds

        # Checks if the timer is finished.
        if (Timer.finishState[userIdentity] == True) or (timeSeconds <= 0):
            await Timer.timerFinish(user, userIdentity)

        # If the timer is not finished then it got paused.
        else:
            await Timer.timerPause(user, userIdentity)

    async def timerPause(user, userIdentity):
        embed = nextcord.Embed(title=(f"Timer"), description=(
            "Your timer is paused."), colour=nextcord.Colour.from_rgb(237, 146, 71))
        Timer.timerMessage[userIdentity] = await user.send(view=TimerButtons.timerPausedView, embed=embed)

    async def timerFinish(user, userIdentity):

        # Takes the amount of time that got studied and assigns it.
        timeSeconds = Timer.timeStudied[userIdentity]
        # Grabbing the description for the message with the amount of time the user studied.
        finishDisplayDescription = await UserInterface.getFinishDisplayDescription(timeSeconds)
        # Grabbing the current date so we can use that in the display message.
        studyDate = date.today()

        embed = nextcord.Embed(title=(f"Finished Session ({studyDate})"), description=(
            finishDisplayDescription), colour=nextcord.Colour.from_rgb(74, 189, 100))

        await user.send(embed=embed)

        from helpers.verification import Verification

        # Removing the user and adding the time to the database.
        await Verification.removeUserVerification(userIdentity)
        await Database.databaseControl(userIdentity, timeSeconds)

        # Deleteing the users values so we can save space.
        del Timer.timerMessage[userIdentity]
        del Timer.finishState[userIdentity]
        del Timer.pauseState[userIdentity]
        del Timer.timeStudied[userIdentity]
        del Timer.timeRemaining[userIdentity]


class TimerButtons():
    def __init__(self, bot):
        self.bot = bot

    async def setTimerButtons(self):

        # Setting the buttons to variables.
        finishButton = Button(label="Finish",
                              style=ButtonStyle.green)
        pauseButton = Button(label="Pause", style=ButtonStyle.red)
        resumeButton = Button(label="Resume", style=ButtonStyle.green)

        # Creating the views.
        TimerButtons.timerButtonView = View(timeout=None)
        TimerButtons.timerButtonView.add_item(finishButton)
        TimerButtons.timerButtonView.add_item(pauseButton)

        TimerButtons.timerPausedView = View(timeout=None)
        TimerButtons.timerPausedView.add_item(resumeButton)

        # Response functions.
        finishButton.callback = TimerButtons.responseFinishButton
        pauseButton.callback = TimerButtons.responsePauseButton
        resumeButton.callback = TimerButtons.responseResumeButton

    ''' The following three functions are all the responses to the buttons
        used in the timer.'''

    async def responseFinishButton(interaction):
        Timer.finishState[interaction.user.id] = True

    async def responsePauseButton(interaction):
        Timer.pauseState[interaction.user.id] = True

    async def responseResumeButton(interaction):
        await Timer.timerMessage[interaction.user.id].delete()
        timeSeconds = Timer.timeRemaining[interaction.user.id]
        Timer.pauseState[interaction.user.id] = False
        await Timer.timerClock(interaction, interaction.user, interaction.user.id, timeSeconds)


# Setup function.
def setup(bot):
    bot.add_cog(Timer(bot))
