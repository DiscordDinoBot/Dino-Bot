import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from helpers.verification import Verification
from .pomodoroClock import PomodoroClock
from .pomodoroCustomInput import PomodoroCustomInput


class PomodoroInput(commands.Cog):

    def __init__(self, bot):

        PomodoroInput.bot = bot
        PomodoroInput.pomodoroClockFile = PomodoroClock(bot)
        PomodoroInput.pomodoroCustomInputFile = PomodoroCustomInput(bot)
        PomodoroInput.VerificationFile = Verification(bot)

        selectionMenuMessage = {}
        removeMessage = {}

        PomodoroInput.removeMessage = removeMessage
        PomodoroInput.selectionMenuMessage = selectionMenuMessage


    # Study command that will run the Selection Menu.

    @commands.command()
    async def study(self, ctx):
        # If the user is in an active session, we will stop the function from continuing.
        if (ctx.author.id) in Verification.sessionActive:
            await Verification.verificationResponse(self, ctx.author, ctx.author.id)
            return

        await Verification.addUserVerification(ctx.author.id)
        PomodoroInput.selectionMenuMessage[ctx.author.id] = await ctx.author.send("Please choose a selection", view=DropdownView())


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
            pomodoroTime = 60
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

        await PomodoroInput.selectionMenuMessage[interaction.user.id].delete()

        # This will run the cancel selection for the menu.
        if (select.values[0] == 'Cancel'):
            Verification.removeUserVerification(interaction.user.id)

        # Custom is selected.
        elif (select.values[0] == "Custom"):
            await PomodoroInput.pomodoroCustomInputFile.pomodoroStudyCustomInput(interaction.user, interaction.user.id)

        # Redirects any other selections to the control file.
        else:
            await PomodoroInput.pomodoroClockFile.setPomodoro(pomodoroTime, shortBreak, longBreak, interaction.user.id)
            await PomodoroInput.pomodoroClockFile.runPomodoro(interaction.user, interaction.user.id)


# Setup function.
def setup(bot):
    bot.add_cog(PomodoroInput(bot))
