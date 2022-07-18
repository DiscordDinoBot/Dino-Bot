import nextcord
import time
import asyncio
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands
from datetime import date


class PomodoroClock(commands.Cog):

    def __init__(self, bot):

        PomodoroClock.bot = bot

        studyDictionary = {}
        breakDictionary = {}
        longBreakDictionary = {}
        sessionState = {}
        pauseState = {}
        skipState = {}
        finishState = {}
        timeRemaining = {}
        resumeState = {}
        pauseMessage = {}
        timeStudied = {}

        PomodoroClock.studyDictionary = studyDictionary
        PomodoroClock.breakDictionary = breakDictionary
        PomodoroClock.longBreakDictionary = longBreakDictionary
        PomodoroClock.sessionState = sessionState
        PomodoroClock.pauseState = pauseState
        PomodoroClock.skipState = skipState
        PomodoroClock.finishState = finishState
        PomodoroClock.timeRemaining = timeRemaining
        PomodoroClock.pauseMessage = pauseMessage
        PomodoroClock.resumeState = resumeState
        PomodoroClock.timeStudied = timeStudied

    async def setPomodoro(self, studyTime, breakTime, longBreakTime, userIdentity):

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

    async def setButtons(self):

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

    async def setSessionState(self, userIdentity):
        if (PomodoroClock.sessionState[userIdentity]) == 7:
            PomodoroClock.sessionState[userIdentity] = 0

        else:
            PomodoroClock.sessionState[userIdentity] += 1

    async def setTimeRemaining(self, userIdentity, timeRemaining):
        PomodoroClock.timeRemaining[userIdentity] = timeRemaining

    async def getDisplayTitle(self, userIdentity):
        if (PomodoroClock.sessionState[userIdentity]) == 7:
            displayTitle = "Long Break"

        elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
            displayTitle = "Break"

        elif(PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            displayTitle = "Study"

        return displayTitle

    async def getDisplayDescription(self, remainingSeconds):

        totalMinute = divmod(remainingSeconds, 60)[0]

        totalHour, totalMinute = divmod(totalMinute, 60)

        # Possibility 1: Multiple hours left.
        if ((totalMinute % 60) == 0) and (totalMinute != 60):
            displayDescription = (f"You have **{totalHour} hours** left.")

        # Possibility 2: 1 hour left.
        elif (totalMinute == 60):
            displayDescription = (f"You have **{totalHour} hour** left.")

        # Possibility 3: Multiple hours and multiple minutes left.
        elif (totalHour > 1) and (totalMinute > 1):
            displayDescription = (
                f"You have **{totalHour} hours** and **{totalMinute} minutes** left.")

        # Possibility 4: 1 hour and multiple minutes left.
        elif (totalHour == 1) and (totalMinute > 1):
            displayDescription = (
                f"You have **{totalHour} hour** and **{totalMinute} minutes** left.")

        # Possibility 5: Multiple hours and one minute left.
        elif (totalHour > 1) and (totalMinute == 1):
            displayDescription = (
                f"You have **{totalHour} hours** and **{totalMinute} minute** left.")

        # Possibility 6: One hour and one minute left.
        elif (totalHour == 1) and (totalMinute == 1):
            displayDescription = (
                f"You have **{totalHour} hour** and **{totalMinute} minute** left.")

        # Possibility 7: Multiple minutes left.
        elif (totalHour < 1) and (totalMinute > 1):
            displayDescription = (f"You have ** {totalMinute} minutes** left.")

        # Possibility 8: Less then a minute left.
        elif (totalHour < 1) and (totalMinute == 1):
            displayDescription = (f"You have less then a **minute** left.")

        return displayDescription

    async def getFinishDisplayDescription(self, totalTime):

        totalMinute, totalSecond = divmod(totalTime, 60)

        totalHour, totalMinute = divmod(totalMinute, 60)

        # Possibility 1: Multiple hours, multiple minutes and multiple seconds finished.
        if (totalHour > 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 2: Multiple hours, multiple minutes and one second finished.
        elif (totalHour > 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 3: Multiple hours, one minute and multiple seconds finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 4: Multiple hours, one minute and one second finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 5: One hour, multiple minutes and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 6: One hour, multiple minutes and one second finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 7: One hour, one minute and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 8: One hour, one minute and one second finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 9: Multiple hours and multiple minutes finished.
        elif (totalHour > 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalMinute} minutes** of studying.")

        # Possibility 10: Multiple hours and one minute finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalMinute} minute** of studying.")

        # Possibility 11: One hour and multiple minutes finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalMinute} minutes** of studying.")

        # Possibility 12: One hour and one minute finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalMinute} minute** of studying.")

        # Possibility 13: Multiple hours and multiple seconds finished.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalSecond} seconds** of studying.")

        # Possibility 14: Multiple hours and one second finished.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalSecond} second** of studying.")

        # Possibility 15: One hour and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalSecond} seconds** of studying.")

        # Possibility 16: One hour and one second finished.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalSecond} second** of studying.")

        # Possibility 17: Multiple minutes and multiple seconds finished.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 18: Multiple minutes and one second finished.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 19: One minute and multiple seconds finished.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 20: One minute and one second finished.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 21: Multiple hours.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours** of studying.")

        # Possibility 22: One hour.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour** of studying.")

        # Possibility 23: Multiple minutes.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes** of studying.")

        # Possibility 24: One minute.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute** of studying.")

        # Possibility 25: Multiple seconds.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalSecond} seconds** of studying.")

        # Possibility 26: One second.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalSecond} second** of studying.")

        # Possibility 27: Zero seconds.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **0 seconds** of studying.")

        return finishDisplayDescription

    async def getDisplayColour(self, userIdentity):
        if (PomodoroClock.sessionState[userIdentity] == 7):
            red = 8
            green = 54
            blue = 133

        elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
            red = 61
            green = 53
            blue = 102

        elif(PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            red = 255
            green = blue = 66

        return red, green, blue

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

    async def responseResumeButton(self):
        PomodoroClock.resumeState[self.user.id] = True
        await PomodoroClock.controlPomodoro(self, self.user, self.user.id)

    async def controlPomodoro(self, user, userIdentity):

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

            await PomodoroClock.pauseMessage[userIdentity].delete()
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

        # Gets all the information for the initial display message
        red, green, blue = await PomodoroClock.getDisplayColour(self, userIdentity)
        displayTitle = await PomodoroClock.getDisplayTitle(self, userIdentity)
        displayDescription = await PomodoroClock.getDisplayDescription(self, timeSeconds)

        # Sets the initial embed message with the variables we recieved above
        embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
            displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))
        # Sends the initial display message and assigns it to a variable so we can edit it in the next loop
        displayMessage = await user.send(view=PomodoroClock.activeSessionButtons, embed=embed)

        initialSeconds = timeSeconds

        while (timeSeconds > 0) and (PomodoroClock.pauseState[userIdentity] == False) and (PomodoroClock.finishState[userIdentity] == False) and (PomodoroClock.skipState[userIdentity] == False):
            await asyncio.sleep(1)

            if ((timeSeconds % 60) == 0):
                red, green, blue = await PomodoroClock.getDisplayColour(self, userIdentity)
                displayTitle = await PomodoroClock.getDisplayTitle(self, userIdentity)
                displayDescription = await PomodoroClock.getDisplayDescription(self, timeSeconds)

                embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
                    displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))
                await displayMessage.edit(view=PomodoroClock.activeSessionButtons, embed=embed)

            timeSeconds -= 1

        if (PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            timeStudied = initialSeconds - timeSeconds
            PomodoroClock.timeStudied[userIdentity] += timeStudied

        await PomodoroClock.setTimeRemaining(self, userIdentity, timeSeconds)

        await displayMessage.delete()

        await PomodoroClock.controlPomodoro(self, user, userIdentity)

    async def pausePomodoro(self, user, userIdentity):
        displayTitle = await PomodoroClock.getDisplayTitle(self, userIdentity)
        embed = nextcord.Embed(title=("Session Paused"), description=(
            f"You have paused your **{displayTitle} session**"), colour=nextcord.Colour.from_rgb(237, 146, 71))

        PomodoroClock.pauseMessage[userIdentity] = await user.send(view=PomodoroClock.pausedSessionButtons, embed=embed)

    async def finishPomodoro(self, user, userIdentity):

        timeSeconds = PomodoroClock.timeStudied[userIdentity]
        finishDisplayDescription = await PomodoroClock.getFinishDisplayDescription(self, timeSeconds)
        studyDate = date.today()

        embed = nextcord.Embed(title=(f"Finished Session ({studyDate})"), description=(
            finishDisplayDescription), colour=nextcord.Colour.from_rgb(74, 189, 100))

        from .pomodoroInput import PomodoroInput
        PomodoroInput.sessionActive[userIdentity] = False

        await user.send(embed=embed)

    async def runPomodoro(self, user, userIdentity):
        await self.setButtons()
        await self.controlPomodoro(user, userIdentity)


# Setup function
def setup(bot):
    bot.add_cog(PomodoroClock(bot))
