import nextcord
from nextcord.ext import commands
from database.database import Database
from helpers.userInterface import UserInterface


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):

        totalTimeStudied = await Database.databaseReceiving(ctx.author.id)

        totalTimeStudiedMessage = (await UserInterface.getFinishDisplayDescription(totalTimeStudied)).strip("You completed of studying.").replace("*", "")
    
        embed = nextcord.Embed(

            title="Study Statistics",
            description="Check out how long you have been studying!",
            colour=nextcord.Colour.from_rgb(109, 157, 255)

        )

        embed.add_field(name="Time Ranges", value=(f"\
        **Today**: {totalTimeStudiedMessage}\n \
        **Past Week**: {totalTimeStudiedMessage}\n \
        **Past Month**: {totalTimeStudiedMessage}\n \
        **Past Year**: {totalTimeStudiedMessage} \n \
        **All Time**: {totalTimeStudiedMessage} \n \
        "),inline="False")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
