import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from .timer import Timer
from helpers.verification import Verification


class TimerInput(commands.Cog):
    def __init__(self, bot):

        TimerInput.bot = bot

        # Sets a dictionary to hold the selection menu message so we can delete the message for that specific user.
        timerSelectionMenuMessage = {}
        TimerInput.timerSelectionMenuMessage = timerSelectionMenuMessage

        TimerInput.timerFile = Timer(bot)

    @nextcord.slash_command(description="Create a timer for studying.")
    async def timer(self, interaction: Interaction):
        # Checks if the user has an active session.
        if (interaction.user.id) in Verification.sessionActive:
            # Sends an ephermeral message to the user incase they are in a server.
            await interaction.response.send_message("You have an active session. Please finish the session to proceed.", ephemeral=True)
            return

        # Adds the user to the active user dictionary.
        await Verification.addUserVerification(interaction.user.id)
        # Assigns the message to the dictionary so we can access the message later in the file.
        TimerInput.timerSelectionMenuMessage[interaction.user.id] = await interaction.user.send("Please choose a selection", view=DropdownView(timeout=None))
        # Sends an ephermeral message to the user incase they are in a server.
        await interaction.response.send_message("Your session has been sent in a private message.", ephemeral=True)


class DropdownView(nextcord.ui.View):

    @nextcord.ui.select(

        placeholder='Choose a timer duration.',

        # Allows only one value to be selected.
        min_values=1,
        max_values=1,

        # Values range is in 5 min increments.
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

        # Convert into an integer and to seconds.
        timerAmount = (int(select.values[0]) * 60)

        # Deletes the selection menu for the timer.
        await TimerInput.timerSelectionMenuMessage[interaction.user.id].delete()

        # Deletes the value that corresponds with the users selection (Saves memory).
        del TimerInput.timerSelectionMenuMessage[interaction.user.id]

        # Setup for the timer and then runs the timer.
        await TimerInput.timerFile.timerSet(interaction.user.id)
        await TimerInput.timerFile.timerMessageSet(interaction.user, interaction.user.id, timerAmount)
        await TimerInput.timerFile.timerClock(interaction.user, interaction.user.id, timerAmount)


# Setup function.
def setup(bot):
    bot.add_cog(TimerInput(bot))
