import nextcord
import asyncio
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands
from datetime import date
from helpers.userInterface import UserInterface
from database.database import Database


class PomodoroClock(commands.Cog):

    def __init__(self, bot):

        PomodoroClock.bot = bot

        PomodoroClock.studyDictionary = {}
        PomodoroClock.breakDictionary = {}
        PomodoroClock.longBreakDictionary = {}
        PomodoroClock.pomodoroMessage = {}
        PomodoroClock.sessionState = {}
        PomodoroClock.pauseState = {}
        PomodoroClock.skipState = {}
        PomodoroClock.finishState = {}
        PomodoroClock.timeRemaining = {}
        PomodoroClock.resumeState = {}
        PomodoroClock.timeStudied = {}

    async def setButtons():

        finishButton = Button(label="Finish", style=ButtonStyle.green)
        pauseButton = Button(label="Pause", style=ButtonStyle.red)
        skipButton = Button(label="Skip", style=ButtonStyle.blurple)
        resumeButton = Button(label="Resume", style=ButtonStyle.green)

        # Button View for any active sessions.
        PomodoroClock.activeSessionButtons = View()
        PomodoroClock.activeSessionButtons.add_item(finishButton)
        PomodoroClock.activeSessionButtons.add_item(pauseButton)
        PomodoroClock.activeSessionButtons.add_item(skipButton)

        # Button View for any paused sessions.
        PomodoroClock.pausedSessionButtons = View()
        PomodoroClock.pausedSessionButtons.add_item(resumeButton)

        # Response functions.
        finishButton.callback = PomodoroClock.responseFinishButton
        pauseButton.callback = PomodoroClock.responsePauseButton
        skipButton.callback = PomodoroClock.responseSkipButton
        resumeButton.callback = PomodoroClock.responseResumeButton

    async def setPomodoro(self, studyTime, breakTime, longBreakTime, user, userIdentity):

        await PomodoroClock.setButtons()

        PomodoroClock.studyDictionary[userIdentity] = studyTime
        PomodoroClock.breakDictionary[userIdentity] = breakTime
        PomodoroClock.longBreakDictionary[userIdentity] = longBreakTime
        PomodoroClock.sessionState[userIdentity] = 0
        PomodoroClock.pauseState[userIdentity] = False
        PomodoroClock.skipState[userIdentity] = False
        PomodoroClock.finishState[userIdentity] = False
        PomodoroClock.resumeState[userIdentity] = False
        PomodoroClock.timeRemaining[userIdentity] = 1
        PomodoroClock.timeStudied[userIdentity] = 0

    async def setSessionState(self, userIdentity):
        if (PomodoroClock.sessionState[userIdentity]) == 7:
            PomodoroClock.sessionState[userIdentity] = 0

        else:
            PomodoroClock.sessionState[userIdentity] += 1

    async def setTimeRemaining(self, userIdentity, timeRemaining):
        PomodoroClock.timeRemaining[userIdentity] = timeRemaining

    async def getSessionState(self, userIdentity):
        return PomodoroClock.sessionState[userIdentity]

    async def getStudyTime(self, userIdentity):
        return PomodoroClock.studyDictionary[userIdentity]

    async def getBreakTime(self, userIdentity):
        return PomodoroClock.breakDictionary[userIdentity]

    async def getLongBreakTime(self, userIdentity):
        return PomodoroClock.longBreakDictionary[userIdentity]

    async def responseFinishButton(self):
        PomodoroClock.finishState[self.user.id] = True

    async def responsePauseButton(self):
        PomodoroClock.pauseState[self.user.id] = True

    async def responseSkipButton(self):
        PomodoroClock.skipState[self.user.id] = True

    async def responseResumeButton(interaction):
        PomodoroClock.resumeState[interaction.user.id] = True
        await PomodoroClock.controlPomodoro(interaction, interaction.user, interaction.user.id)

    async def controlPomodoro(self, user, userIdentity):

        try:
            await PomodoroClock.pomodoroMessage[userIdentity].delete()

        except (nextcord.errors.NotFound, KeyError):
            pass

        # Checks if the user wants to skip the state
        if (PomodoroClock.skipState[userIdentity] == True):
            PomodoroClock.skipState[userIdentity] = False
            await PomodoroClock.setSessionState(self, userIdentity)

        # Checks if the session state is complete
        if (PomodoroClock.timeRemaining[userIdentity] <= 0):
            await PomodoroClock.setSessionState(self, userIdentity)

        # Checks if the user wants to resume the session
        if (PomodoroClock.resumeState[userIdentity] == True):

            PomodoroClock.pauseState[userIdentity] = False
            PomodoroClock.resumeState[userIdentity] = False
            timeSeconds = PomodoroClock.timeRemaining[userIdentity]
            await PomodoroClock.clockPomodoro(self, user, userIdentity, timeSeconds)

        # Checks if user has paused the session
        elif (PomodoroClock.pauseState[userIdentity] == True):
            await PomodoroClock.pausePomodoro(self, user, userIdentity)

        # Checks if user has finished the session
        elif (PomodoroClock.finishState[userIdentity] == True):
            await PomodoroClock.finishPomodoro(self, user, userIdentity)

        # Checks if the user wants to run a study session
        elif (PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            timeSeconds = await PomodoroClock.getStudyTime(self, userIdentity)
            await PomodoroClock.clockPomodoro(self, user, userIdentity, timeSeconds)

        # Checks if user wants to run a break session
        elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
            timeSeconds = await PomodoroClock.getBreakTime(self, userIdentity)
            await PomodoroClock.clockPomodoro(self, user, userIdentity, timeSeconds)

        # Checks if user wants to run a long break session
        elif (PomodoroClock.sessionState[userIdentity]) == 7:
            timeSeconds = await PomodoroClock.getLongBreakTime(self, userIdentity)
            await PomodoroClock.clockPomodoro(self, user, userIdentity, timeSeconds)

    async def clockPomodoro(self, user, userIdentity, timeSeconds):

        red, green, blue = await UserInterface.getDisplayColour(PomodoroClock.sessionState[userIdentity])
        displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
        displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

        embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
            displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))
        PomodoroClock.pomodoroMessage[userIdentity] = await user.send(view=PomodoroClock.activeSessionButtons, embed=embed)

        initialSeconds = timeSeconds

        while (timeSeconds > 0) and (PomodoroClock.pauseState[userIdentity] == False) and (PomodoroClock.finishState[userIdentity] == False) and (PomodoroClock.skipState[userIdentity] == False):
            await asyncio.sleep(1)

            if ((timeSeconds % 60) == 0):
                red, green, blue = await UserInterface.getDisplayColour(PomodoroClock.sessionState[userIdentity])
                displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
                displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

                embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
                    displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))
                await PomodoroClock.pomodoroMessage[userIdentity].edit(view=PomodoroClock.activeSessionButtons, embed=embed)

            timeSeconds -= 1

        if (PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            timeStudied = initialSeconds - timeSeconds
            PomodoroClock.timeStudied[userIdentity] += timeStudied

        await PomodoroClock.setTimeRemaining(self, userIdentity, timeSeconds)

        await PomodoroClock.controlPomodoro(self, user, userIdentity)

    async def pausePomodoro(self, user, userIdentity):
        displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
        embed = nextcord.Embed(title=("Session Paused"), description=(
            f"You have paused your **{displayTitle} session**"), colour=nextcord.Colour.from_rgb(237, 146, 71))

        PomodoroClock.pomodoroMessage[userIdentity] = await user.send(view=PomodoroClock.pausedSessionButtons, embed=embed)

    async def finishPomodoro(self, user, userIdentity):

        timeSeconds = PomodoroClock.timeStudied[userIdentity]
        finishDisplayDescription = await UserInterface.getFinishDisplayDescription(timeSeconds)
        studyDate = date.today()

        embed = nextcord.Embed(title=(f"Finished Session ({studyDate})"), description=(
            finishDisplayDescription), colour=nextcord.Colour.from_rgb(74, 189, 100))

        from helpers.verification import Verification

        await Verification.removeUserVerification(userIdentity)

        await user.send(view=None, embed=embed)

        await Database.databaseInsertion(userIdentity, timeSeconds)

        # Removes all user data from the dictionarys
        del PomodoroClock.studyDictionary[userIdentity]
        del PomodoroClock.breakDictionary[userIdentity]
        del PomodoroClock.longBreakDictionary[userIdentity]
        del PomodoroClock.sessionState[userIdentity]
        del PomodoroClock.pauseState[userIdentity]
        del PomodoroClock.skipState[userIdentity]
        del PomodoroClock.finishState[userIdentity]
        del PomodoroClock.resumeState[userIdentity]
        del PomodoroClock.timeRemaining[userIdentity]
        del PomodoroClock.timeStudied[userIdentity]

    async def runPomodoro(self, user, userIdentity):
        await self.controlPomodoro(user, userIdentity)


# Setup function
def setup(bot):
    bot.add_cog(PomodoroClock(bot))
