import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that runs the content for the help command.
    @nextcord.slash_command(description="Provides instructions on how to use the bot.")
    async def help(self, interaction: Interaction):

        embed = nextcord.Embed(

            title="Dino Bot",
            description="This is the offical Dino Bot, the best tool used for having focused study sessions.",
            colour=nextcord.Colour.from_rgb(109, 157, 255)

        )

        # Fields that are added to the main embed above this comment.
        embed.add_field(name="Commands", value="`/stats` Displays the amount of time the user has studied (PST Time).\
            \n`/study` Initiates the study session and opens the session menu. \
            \n`/timer` Creates a timer for the user and opens a timer selection menu.", inline="False")

        embed.add_field(
            name="Information", value="Check out the [website](https://dinosaurbot.com) to learn more!")

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))
