import nextcord
from nextcord.ext import commands

from .pomodoroClock import PomodoroClock

#Class that takes in the input from Selection Menu for the bot.
class PomodoroCustomInput(commands.Cog):
    def __init__(self, bot):
    
        PomodoroCustomInput.bot = bot
        PomodoroCustomInput.pomodoroClockFile = PomodoroClock(bot)

        customSelectionMenuMessage = {}
        customSelectionState = {}

        PomodoroCustomInput.customSelectionMenuMessage = customSelectionMenuMessage
        PomodoroCustomInput.customSelectionState = customSelectionState
    
    async def pomodoroStudyCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionState[userIdentity] = 0
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Study** session duration" , view = DropdownView())

    async def pomodoroBreakCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Break** session duration" , view = DropdownView())

    async def pomodoroLongBreakCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Long Break** session duration" , view = DropdownView())


    async def getSessionState(self, userIdentity):
        if (PomodoroCustomInput.customSelectionState[userIdentity] == 0):
            state = 0
        
        elif (PomodoroCustomInput.customSelectionState[userIdentity] == 1):
            placeHolder = "Select a break time."
        
        else:
            placeHolder = "Select a long break time."
        
        return placeHolder


class DropdownView(nextcord.ui.View):

    @nextcord.ui.select(
            
        placeholder="Select a session time", 
        min_values=1, 
        max_values=1,

        options = [

            nextcord.SelectOption(
                label="5 Minutes",
                value = 5),
            
            nextcord.SelectOption(
                label="10 Minutes",
                value = 10),
            
            nextcord.SelectOption(
                label="15 Minutes",
                value = 15),
            
            nextcord.SelectOption(
                label="20 Minutes",
                value = 20),
            
            nextcord.SelectOption(
                label="25 Minutes",
                value = 20),
            
        ]
    )

    #This is the callback function that will run once the selection has been made from the user.
    async def callback(self, select, interaction: nextcord.Interaction):
        pass

#Setup function.
def setup(bot):
  bot.add_cog(PomodoroCustomInput(bot))