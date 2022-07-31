from nextcord.ext import commands

# Class used to tell the user what version the bot is running on.


class Version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Version command that prints the version of the bot to the user.
    @commands.command()
    async def version(self, ctx):
        # <--- CHANGE VERSION NUMBER HERE
        await ctx.send("Dino Bot is running on version **0.5.5**")


def setup(bot):
    bot.add_cog(Version(bot))
