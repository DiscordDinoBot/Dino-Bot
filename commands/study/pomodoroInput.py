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

        # Dictionary for the selection menu message so we can delete it at the end.
        PomodoroInput.selectionMenuMessage = {}

    @nextcord.slash_command(description="Create a Pomodoro session for studying.")
    async def study(self, interaction: Interaction):
        
        #Checks if the user has an active session
        if (interaction.user.id) in Verification.sessionActive:
            #If the message is not in a private channel we must send it secretly (Ephemeral)
            if (interaction.channel.type is not nextcord.ChannelType.private):
                await interaction.response.send_message("You have an active session. Please finish the session to proceed.", ephemeral=True)
            #Message is sent in private channel therefore we send it not ephemeral.
            else:
                await interaction.response.send_message("You have an active session. Please finish the session to proceed.")
            #Stops the function from continuing so we dont start the session.
            return

        # If the user is not in an active session we add them to the dictionary.
        await Verification.addUserVerification(interaction.user.id)

        #Checks if the channel is not a private channel.
        if (interaction.channel.type is not nextcord.ChannelType.private):
            #We send a secret message alongside the selection menu.
            PomodoroInput.selectionMenuMessage[interaction.user.id] = await interaction.user.send("Please choose a selection", view=DropdownView(timeout=None))
            await interaction.response.send_message("Your session has been sent in a private message.", ephemeral=True)
        
        #Channel is private so we do not need to notify the user with a secret message.
        else:
            PomodoroInput.selectionMenuMessage[interaction.user.id] = await interaction.response.send_message("Please choose a selection", view=DropdownView(timeout=None))

class DropdownView(nextcord.ui.View):
    @nextcord.ui.select(

        placeholder='Select a studying time.',

        # Allows only one value to be selected.
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

        # Removes the message from Discord
        await PomodoroInput.selectionMenuMessage[interaction.user.id].delete()

        # Removes the message from the Dictionary
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
