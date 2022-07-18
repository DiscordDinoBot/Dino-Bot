import nextcord
from nextcord.ext import commands

# Custom Help command that can display instructions for the user


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command that runs the content for the help command
    @commands.command()
    async def help(self, ctx):

        embed = nextcord.Embed(

            title="Dino Bot",
            description="This is the offical Dino Bot, the best tool used for having focused study sessions.",
            colour=nextcord.Colour.from_rgb(109, 157, 255)

        )

        embed.add_field(name="Commands", value="`!study`\n Initiates the study timer and opens the study timer menu\n`!version`\n Displays the bot's version that it's running on\n`!help`\n Displays the bot's commands and guidelines",
                        inline="False")

        # Leave alone:
        await ctx.author.send(embed=embed)

# Setup function


def setup(bot):
    bot.add_cog(Help(bot))
