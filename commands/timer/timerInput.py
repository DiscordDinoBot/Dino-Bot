import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from .timer import Timer
from helpers.verification import Verification


class TimerInput(commands.Cog):
    def __init__(self, bot):

        TimerInput.bot = bot

        timerSelectionMenuMessage = {}
        TimerInput.timerSelectionMenuMessage = timerSelectionMenuMessage

        TimerInput.timerFile = Timer(bot)

    @nextcord.slash_command(description="Create a timer for studying.")
    async def timer(self, interaction: Interaction):
        if (interaction.user.id) in Verification.sessionActive:
            await Verification.verificationResponse(self, interaction.user, interaction.user.id)
            await interaction.response.send_message("You have an active session. Please check private messages to proceed.", ephemeral=True)
            return

        await Verification.addUserVerification(interaction.user.id)
        TimerInput.timerSelectionMenuMessage[interaction.user.id] = await interaction.user.send("Please choose a selection", view=DropdownView(timeout=None))
        await interaction.response.send_message("Your session has been sent in a private message.", ephemeral=True)

class DropdownView(nextcord.ui.View):

    @nextcord.ui.select(

        placeholder='Choose a timer duration.',
        min_values=1,
        max_values=1,

        options=[

            nextcord.SelectOption(
                label="1 Minute",
                value=1),

            nextcord.SelectOption(
                label="2 Minutes",
                value=2),

            nextcord.SelectOption(
                label="3 Minutes",
                value=3),

            nextcord.SelectOption(
                label="4 Minutes",
                value=4),

            nextcord.SelectOption(
                label="5 Minutes",
                value=5),

            nextcord.SelectOption(
                label="6 Minutes",
                value=6),

            nextcord.SelectOption(
                label="7 Minutes",
                value=7),

            nextcord.SelectOption(
                label="8 Minutes",
                value=8),

            nextcord.SelectOption(
                label="9 Minutes",
                value=9),

            nextcord.SelectOption(
                label="10 Minutes",
                value=10),

            nextcord.SelectOption(
                label="11 Minutes",
                value=11),

            nextcord.SelectOption(
                label="12 Minutes",
                value=12),

            nextcord.SelectOption(
                label="13 Minutes",
                value=13),

            nextcord.SelectOption(
                label=f"14 Minutes",
                value=14),

            nextcord.SelectOption(
                label=f"15 Minutes",
                value=15),

            nextcord.SelectOption(
                label="16 Minutes",
                value=16),

            nextcord.SelectOption(
                label="17 Minutes",
                value=17),

            nextcord.SelectOption(
                label=f"18 Minutes",
                value=18),

            nextcord.SelectOption(
                label=f"19 Minutes",
                value=19),

            nextcord.SelectOption(
                label="20 Minutes",
                value=20),

            nextcord.SelectOption(
                label="21 Minutes",
                value=21),

            nextcord.SelectOption(
                label="22 Minutes",
                value=22),

            nextcord.SelectOption(
                label="23 Minutes",
                value=23),

            nextcord.SelectOption(
                label="24 Minutes",
                value=24),

            nextcord.SelectOption(
                label="25 Minutes",
                value=25),

        ]
    )
    # This is the callback function that will run once the selection has been made from the user.
    async def callback(self, select, interaction: nextcord.Interaction):

        # Convert into an integer and to seconds
        timerAmount = (int(select.values[0]) * 60)

        await TimerInput.timerSelectionMenuMessage[interaction.user.id].delete()

        del TimerInput.timerSelectionMenuMessage[interaction.user.id]

        await TimerInput.timerFile.timerSet(interaction.user.id)
        await TimerInput.timerFile.timerClock(interaction.user, interaction.user.id, timerAmount)


# Setup function.
def setup(bot):
    bot.add_cog(TimerInput(bot))
