import nextcord
from nextcord.ext import commands
from nextcord import Interaction

# Custom Help command that can display instructions for the user


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that runs the content for the help command
    @nextcord.slash_command(description="Provides instructions on how to use the bot.",guild_ids=[674092094364844055])
    async def help(self, interaction: Interaction):

        embed = nextcord.Embed(

            title="Dino Bot",
            description="This is the offical Dino Bot, the best tool used for having focused study sessions.",
            colour=nextcord.Colour.from_rgb(109, 157, 255)

        )

        embed.add_field(name="Commands", value="`!study`\n Initiates the study timer and opens the study timer menu\n`!version`\n Displays the bot's version that it's running on\n`!help`\n Displays the bot's commands and guidelines",
                        inline="False")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))
