import nextcord
from nextcord.ext import commands

from commands.study.pomodoroClock import PomodoroClock
from commands.study.pomodoroCustomInput import PomodoroCustomInput
from commands.study.pomodoroInput import PomodoroInput


class Buttons(commands.Cog):
    def __init__(self, bot):
    
        self.bot = bot


    #INSERT ALL BUTTONS FOR THE BOT


#Setup function.
def setup(bot):
  bot.add_cog(Buttons(bot))