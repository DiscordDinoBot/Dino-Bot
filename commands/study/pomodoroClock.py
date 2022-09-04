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

        # Dictionaries used to contain the variables used in the clock.
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

        # Settings the button to a variable and adding the styles to the buttons.
        finishButton = Button(label="Finish", style=ButtonStyle.green)
        pauseButton = Button(label="Pause", style=ButtonStyle.red)
        skipButton = Button(label="Skip", style=ButtonStyle.blurple)
        resumeButton = Button(label="Resume", style=ButtonStyle.green)

        # Button View for any active sessions.
        PomodoroClock.activeSessionButtons = View(timeout=None)
        PomodoroClock.activeSessionButtons.add_item(finishButton)
        PomodoroClock.activeSessionButtons.add_item(pauseButton)
        PomodoroClock.activeSessionButtons.add_item(skipButton)

        # Button View for any paused sessions.
        PomodoroClock.pausedSessionButtons = View(timeout=None)
        PomodoroClock.pausedSessionButtons.add_item(resumeButton)

        # Response functions.
        finishButton.callback = PomodoroClock.responseFinishButton
        pauseButton.callback = PomodoroClock.responsePauseButton
        skipButton.callback = PomodoroClock.responseSkipButton
        resumeButton.callback = PomodoroClock.responseResumeButton

    async def setPomodoro(self, studyTime, breakTime, longBreakTime, user, userIdentity):

        # Running the function that will assign all the buttons.
        await PomodoroClock.setButtons()

        # Adding all the users values the dictionaries we created above.
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
        # Checking if the state has passed the long break. If it has we must reset it.
        if (PomodoroClock.sessionState[userIdentity]) == 7:
            PomodoroClock.sessionState[userIdentity] = 0

        # Moving the user to the next session state.
        else:
            PomodoroClock.sessionState[userIdentity] += 1

    # Setting the time remaining so we can access it when we resume the clock.
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

    ''' The following four functions are all the responses for the 
        buttons that we use in the clock. This will set the value in the 
        dictionary to True.'''

    async def responseFinishButton(self):
        PomodoroClock.finishState[self.user.id] = True

    async def responsePauseButton(self):
        PomodoroClock.pauseState[self.user.id] = True

    async def responseSkipButton(self):
        PomodoroClock.skipState[self.user.id] = True

    async def responseResumeButton(interaction):
        PomodoroClock.resumeState[interaction.user.id] = True
        # We must manual run the controlPomodoro function since we dont use a while loop in the pause funciton.
        await PomodoroClock.controlPomodoro(interaction, interaction.user, interaction.user.id)

    async def controlPomodoro(self, user, userIdentity):

        # We attempt to delete the pomodoro message incase a session was active.
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

        # Following three variables all receive the UI from the UI file.
        red, green, blue = await UserInterface.getDisplayColour(PomodoroClock.sessionState[userIdentity])
        displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
        displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

        # Setting up the embed for the clock message.
        embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
            displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))

        # Assigning the clock message to a variable so we can delete it when the clock is finished or paused.
        PomodoroClock.pomodoroMessage[userIdentity] = await user.send(view=PomodoroClock.activeSessionButtons, embed=embed)

        # Keeping track of the initalTime so we can see how much time elasped.
        initialSeconds = timeSeconds

        while (timeSeconds > 0) and (PomodoroClock.pauseState[userIdentity] == False) and (PomodoroClock.finishState[userIdentity] == False) and (PomodoroClock.skipState[userIdentity] == False):
            await asyncio.sleep(1)

            # Checks if a minute has passed. If this is true we must update the display of the clock.
            if ((timeSeconds % 60) == 0):
                red, green, blue = await UserInterface.getDisplayColour(PomodoroClock.sessionState[userIdentity])
                displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
                displayDescription = await UserInterface.getDisplayDescription(timeSeconds)

                embed = nextcord.Embed(title=(f"{displayTitle} Session"), description=(
                    displayDescription), colour=nextcord.Colour.from_rgb(red, green, blue))
                await PomodoroClock.pomodoroMessage[userIdentity].edit(view=PomodoroClock.activeSessionButtons, embed=embed)

            timeSeconds -= 1

        # Checks if the session state was a study state. If True we add the time to the studied variable.
        if (PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
            timeStudied = initialSeconds - timeSeconds
            PomodoroClock.timeStudied[userIdentity] += timeStudied

        await PomodoroClock.setTimeRemaining(self, userIdentity, timeSeconds)

        # Running the control function that will determine which state the user needs.
        await PomodoroClock.controlPomodoro(self, user, userIdentity)

    async def pausePomodoro(self, user, userIdentity):
        displayTitle = await UserInterface.getDisplayTitle(PomodoroClock.sessionState[userIdentity])
        embed = nextcord.Embed(title=("Session Paused"), description=(
            f"You have paused your **{displayTitle} session**"), colour=nextcord.Colour.from_rgb(237, 146, 71))

        # Simply sends the message to the user stating the session is paused.
        PomodoroClock.pomodoroMessage[userIdentity] = await user.send(view=PomodoroClock.pausedSessionButtons, embed=embed)

    async def finishPomodoro(self, user, userIdentity):

        # Grabs the amount of time that was studied.
        timeSeconds = PomodoroClock.timeStudied[userIdentity]
        # Grabbing the description for the message with the amount of time the user studied.
        finishDisplayDescription = await UserInterface.getFinishDisplayDescription(timeSeconds)
        # Grabbing the current date so we can use that in the display message.
        studyDate = date.today()

        embed = nextcord.Embed(title=(f"Finished Session ({studyDate})"), description=(
            finishDisplayDescription), colour=nextcord.Colour.from_rgb(74, 189, 100))

        # Importation in here due to circular import.
        from helpers.verification import Verification

        # Removing the user so they can start another session.
        await Verification.removeUserVerification(userIdentity)

        await user.send(view=None, embed=embed)

        # Passing the amount of time studied to the database so we can add it in.
        await Database.databaseControl(userIdentity, timeSeconds)

        # Removes all user data from the dictionaries to save space.
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
        del PomodoroClock.pomodoroMessage[userIdentity]

    async def runPomodoro(self, user, userIdentity):
        await self.controlPomodoro(user, userIdentity)


def setup(bot):
    bot.add_cog(PomodoroClock(bot))
