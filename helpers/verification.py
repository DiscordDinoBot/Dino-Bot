import nextcord
from nextcord.ext import commands

from commands.study.pomodoroClock import PomodoroClock
from commands.study.pomodoroCustomInput import PomodoroCustomInput
from commands.study.pomodoroInput import PomodoroInput


class Verification(commands.Cog):
    def __init__(self, bot):
    
        self.bot = bot

        Verification.sessionActive = {}
        
        Verification.pomodoroClockFile = PomodoroClock(bot)
        Verification.pomodoroCustomInputFile = PomodoroCustomInput(bot)
        Verification.pomodoroInputFile = PomodoroInput(bot)


    #INSERT ALL VERIFICATION ASPECTS TO THE BOT


#Setup function.
def setup(bot):
  bot.add_cog(Verification(bot))