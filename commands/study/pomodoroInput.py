import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from helpers.verification import Verification
from .pomodoroClock import PomodoroClock
from .pomodoroCustomInput import PomodoroCustomInput


class PomodoroInput(commands.Cog):

    def __init__(self, bot):

        PomodoroInput.bot = bot
        PomodoroInput.pomodoroClockFile = PomodoroClock(bot)
        PomodoroInput.pomodoroCustomInputFile = PomodoroCustomInput(bot)
        PomodoroInput.VerificationFile = Verification(bot)

        PomodoroInput.selectionMenuMessage = {}
    
    @nextcord.slash_command(description="Create a Pomodoro session for studying.",guild_ids=[674092094364844055])
    async def study(self, interaction: Interaction):
    
        # If the user is in an active session, we will stop the function from continuing.
        if (interaction.user.id) in Verification.sessionActive:
            await Verification.verificationResponse(self, interaction.user, interaction.user.id)
            await interaction.response.send_message("You have an active session. Please check private messages to proceed.", ephemeral=True)
            return

        await Verification.addUserVerification(interaction.user.id)
        PomodoroInput.selectionMenuMessage[interaction.user.id] = await interaction.user.send("Please choose a selection", view=DropdownView(timeout=None))
        await interaction.response.send_message("Your session has been sent in a private message.", ephemeral=True)

class DropdownView(nextcord.ui.View):
    @nextcord.ui.select(

        placeholder='Select a studying time.',
        min_values=1,
        max_values=1,

        options=[

            # BEGINNER

            nextcord.SelectOption(
                label="Beginner",
                emoji="🟩",
                description="Study: 15 Mins | Break: 5 Mins | Long Break: 15 Mins",
                value='Beginner'),

            # INTERMEDIATE

            nextcord.SelectOption(
                label="Intermediate",
                emoji="🟧",
                description="Study: 35 Mins | Break: 5 Mins | Long Break: 15 Mins",
                value='Intermediate'),

            # EXPERT

            nextcord.SelectOption(
                label="Expert",
                emoji="🟥",
                description="Study: 45 Mins | Break: 5 Mins | Long Break: 20 Mins",
                value='Expert'),

            # REGULAR

            nextcord.SelectOption(
                label="Regular",
                emoji="⬜",
                description="Study: 25 Mins | Break: 5 Mins | Long Break: 15 Mins",
                value='Regular'),

            # CUSTOM

            nextcord.SelectOption(
                label="Custom",
                emoji="⚙️",
                description="Choose your own times.",
                value='Custom'),

            # CANCEL

            nextcord.SelectOption(
                label="Cancel",
                emoji="❌",
                value='Cancel')
        ]
    )
    # This is the callback function that will run once the selection has been made from the user.
    async def callback(self, select, interaction: nextcord.Interaction):

        '''
        All the following variables are in seconds.

        pomodoroTime is the study time.
        shortBreak is the short break time.
        longBreak is the long break time.
        '''

        # Beginner is selected.
        if (select.values[0] == "Beginner"):
            pomodoroTime = 900
            shortBreak = 300
            longBreak = 900

        # Intermediate is selected.
        elif (select.values[0] == "Intermediate"):
            pomodoroTime = 2100
            shortBreak = 300
            longBreak = 900

        # Expert is selected.
        elif (select.values[0] == "Expert"):
            pomodoroTime = 2700
            shortBreak = 300
            longBreak = 1200

        # Regular is selected.
        elif (select.values[0] == "Regular"):
            pomodoroTime = 1500
            shortBreak = 300
            longBreak = 900

        #Removes the message from Discord
        await PomodoroInput.selectionMenuMessage[interaction.user.id].delete()

        #Removes the message from the Dictionary
        del PomodoroInput.selectionMenuMessage[interaction.user.id]

        # This will run the cancel selection for the menu.
        if (select.values[0] == 'Cancel'):
            await Verification.removeUserVerification(interaction.user.id)

        # Custom is selected.
        elif (select.values[0] == "Custom"):
            await PomodoroInput.pomodoroCustomInputFile.pomodoroStudyCustomInput(interaction.user, interaction.user.id)

        # Redirects any other selections to the control file.
        else:
            await PomodoroInput.pomodoroClockFile.setPomodoro(pomodoroTime, shortBreak, longBreak, interaction.user, interaction.user.id)
            await PomodoroInput.pomodoroClockFile.runPomodoro(interaction.user, interaction.user.id)


# Setup function.
def setup(bot):
    bot.add_cog(PomodoroInput(bot))
