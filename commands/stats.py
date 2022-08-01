from discord import Interaction
import nextcord
from nextcord.ext import commands
from database.database import Database
from helpers.userInterface import UserInterface


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Showcases the amount of time that you have studied.",guild_ids=[1003759523674210416])
    async def stats(self, interaction: Interaction):

        totalTimeStudied = await Database.databaseReceiving(interaction.user.id)

        totalTimeStudiedMessage = (await UserInterface.getFinishDisplayDescription(totalTimeStudied)).strip("You completed of studying.").replace("*", "")
    
        embed = nextcord.Embed(

            title="Study Statistics",
            description=f"Check out how long {interaction.user.mention} has been studying!",
            colour=nextcord.Colour.from_rgb(109, 157, 255)

        )

        embed.add_field(name="Time Ranges", value=(f"\
        **Today**: {totalTimeStudiedMessage}\n \
        **Past Week**: {totalTimeStudiedMessage}\n \
        **Past Month**: {totalTimeStudiedMessage}\n \
        **Past Year**: {totalTimeStudiedMessage} \n \
        **All Time**: {totalTimeStudiedMessage} \n \
        "),inline="False")

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
