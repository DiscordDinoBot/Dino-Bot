import nextcord
from nextcord.ext import commands
from .pomodoroClock import PomodoroClock


class PomodoroCustomInput(commands.Cog):
    def __init__(self, bot):

        PomodoroCustomInput.bot = bot
        PomodoroCustomInput.pomodoroClockFile = PomodoroClock(bot)

        customSelectionMenuMessage = {}
        customSelectionState = {}
        studyTime = {}
        breakTime = {}

        PomodoroCustomInput.customSelectionMenuMessage = customSelectionMenuMessage
        PomodoroCustomInput.customSelectionState = customSelectionState
        PomodoroCustomInput.studyTime = studyTime
        PomodoroCustomInput.breakTime = breakTime

    async def pomodoroStudyCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionState[userIdentity] = 0
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Study** session duration", view=DropdownView())

    async def pomodoroBreakCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Break** session duration", view=DropdownView())

    async def pomodoroLongBreakCustomInput(self, user, userIdentity):
        PomodoroCustomInput.customSelectionMenuMessage[userIdentity] = await user.send("Choose a **Long Break** session duration", view=DropdownView())


class DropdownView(nextcord.ui.View):

    @nextcord.ui.select(

        placeholder="Select a session time",
        min_values=1,
        max_values=1,

        options=[

            nextcord.SelectOption(
                label="5 Minutes",
                value=5),

            nextcord.SelectOption(
                label="10 Minutes",
                value=10),

            nextcord.SelectOption(
                label="15 Minutes",
                value=15),

            nextcord.SelectOption(
                label="20 Minutes",
                value=20),

            nextcord.SelectOption(
                label="25 Minutes",
                value=25),

            nextcord.SelectOption(
                label="30 Minutes",
                value=30),

            nextcord.SelectOption(
                label="40 Minutes",
                value=40),

            nextcord.SelectOption(
                label="45 Minutes",
                value=45),

            nextcord.SelectOption(
                label="50 Minutes",
                value=50),

            nextcord.SelectOption(
                label="55 Minutes",
                value=55),

            nextcord.SelectOption(
                label="1 Hour",
                value=60),

            nextcord.SelectOption(
                label="1 Hour and 5 Minutes",
                value=65),

            nextcord.SelectOption(
                label="1 Hour and 10 Minutes",
                value=70),

            nextcord.SelectOption(
                label="1 Hour and 15 Minutes",
                value=75),

            nextcord.SelectOption(
                label="1 Hour and 20 Minutes",
                value=80),

            nextcord.SelectOption(
                label="1 Hour and 25 Minutes",
                value=85),

            nextcord.SelectOption(
                label="1 Hour and 30 Minutes",
                value=90),

            nextcord.SelectOption(
                label="1 Hour and 35 Minutes",
                value=95),

            nextcord.SelectOption(
                label="1 Hour and 40 Minutes",
                value=100),

            nextcord.SelectOption(
                label="1 Hour and 45 Minutes",
                value=105),

            nextcord.SelectOption(
                label="1 Hour and 50 Minutes",
                value=110),

            nextcord.SelectOption(
                label="1 Hour and 55 Minutes",
                value=115),

            nextcord.SelectOption(
                label="2 Hours",
                value=120),
        ]
    )
    # This is the callback function that will run once the selection has been made from the user.
    async def callback(self, select, interaction: nextcord.Interaction):

        # Convert into an integer and to seconds
        userValue = (int(select.values[0]) * 60)

        # Runs if the study time is the current session state
        if (PomodoroCustomInput.customSelectionState[interaction.user.id] == 0):
            # Assigns the selection to the study time for the user
            PomodoroCustomInput.studyTime[interaction.user.id] = (userValue)
            # Increasing the session state
            PomodoroCustomInput.customSelectionState[interaction.user.id] += 1

            # Deletes previous message
            await PomodoroCustomInput.customSelectionMenuMessage[interaction.user.id].delete()
            # Calls upon the break message to be called
            await PomodoroCustomInput.pomodoroBreakCustomInput(self, interaction.user, interaction.user.id)

        # Runs if the break time is the current session state
        elif(PomodoroCustomInput.customSelectionState[interaction.user.id] == 1):
            # Assigns the selection to the break time for the user
            PomodoroCustomInput.breakTime[interaction.user.id] = (userValue)
            # Increasing the session state
            PomodoroCustomInput.customSelectionState[interaction.user.id] += 1

            # Deletes previous message
            await PomodoroCustomInput.customSelectionMenuMessage[interaction.user.id].delete()
            await PomodoroCustomInput.pomodoroLongBreakCustomInput(self, interaction.user, interaction.user.id)

        # Runs if the long break time is the current session state
        else:
            # Grabs all the values so we can send it to the pomodoroClock file
            pomodoroTime = PomodoroCustomInput.studyTime[interaction.user.id]
            shortBreak = PomodoroCustomInput.breakTime[interaction.user.id]
            longBreak = userValue

            # Deletes previous message
            await PomodoroCustomInput.customSelectionMenuMessage[interaction.user.id].delete()

            # Runs the pomodoro clock file with the session times collected
            await PomodoroCustomInput.pomodoroClockFile.setPomodoro(pomodoroTime, shortBreak, longBreak, interaction.user.id)
            await PomodoroCustomInput.pomodoroClockFile.runPomodoro(interaction.user, interaction.user.id)


def setup(bot):
    bot.add_cog(PomodoroCustomInput(bot))
