from nextcord.ext import commands


class UserInterface(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def getFinishDisplayDescription(self, totalTime):

        totalMinute, totalSecond = divmod(totalTime, 60)

        totalHour, totalMinute = divmod(totalMinute, 60)

        # Possibility 1: Multiple hours, multiple minutes and multiple seconds finished.
        if (totalHour > 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 2: Multiple hours, multiple minutes and one second finished.
        elif (totalHour > 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 3: Multiple hours, one minute and multiple seconds finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 4: Multiple hours, one minute and one second finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours, {totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 5: One hour, multiple minutes and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 6: One hour, multiple minutes and one second finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 7: One hour, one minute and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 8: One hour, one minute and one second finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour, {totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 9: Multiple hours and multiple minutes finished.
        elif (totalHour > 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalMinute} minutes** of studying.")

        # Possibility 10: Multiple hours and one minute finished.
        elif (totalHour > 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalMinute} minute** of studying.")

        # Possibility 11: One hour and multiple minutes finished.
        elif (totalHour == 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalMinute} minutes** of studying.")

        # Possibility 12: One hour and one minute finished.
        elif (totalHour == 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalMinute} minute** of studying.")

        # Possibility 13: Multiple hours and multiple seconds finished.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalSecond} seconds** of studying.")

        # Possibility 14: Multiple hours and one second finished.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours and {totalSecond} second** of studying.")

        # Possibility 15: One hour and multiple seconds finished.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalSecond} seconds** of studying.")

        # Possibility 16: One hour and one second finished.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour and {totalSecond} second** of studying.")

        # Possibility 17: Multiple minutes and multiple seconds finished.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes and {totalSecond} seconds** of studying.")

        # Possibility 18: Multiple minutes and one second finished.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes and {totalSecond} second** of studying.")

        # Possibility 19: One minute and multiple seconds finished.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute and {totalSecond} seconds** of studying.")

        # Possibility 20: One minute and one second finished.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute and {totalSecond} second** of studying.")

        # Possibility 21: Multiple hours.
        elif (totalHour > 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hours** of studying.")

        # Possibility 22: One hour.
        elif (totalHour == 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalHour} hour** of studying.")

        # Possibility 23: Multiple minutes.
        elif (totalHour < 1) and (totalMinute > 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minutes** of studying.")

        # Possibility 24: One minute.
        elif (totalHour < 1) and (totalMinute == 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **{totalMinute} minute** of studying.")

        # Possibility 25: Multiple seconds.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond > 1):
            finishDisplayDescription = (
                f"You completed **{totalSecond} seconds** of studying.")

        # Possibility 26: One second.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond == 1):
            finishDisplayDescription = (
                f"You completed **{totalSecond} second** of studying.")

        # Possibility 27: Zero seconds.
        elif (totalHour < 1) and (totalMinute < 1) and (totalSecond < 1):
            finishDisplayDescription = (
                f"You completed **0 seconds** of studying.")

        return finishDisplayDescription

    async def getDisplayDescription(self, remainingSeconds):

        totalMinute = divmod(remainingSeconds, 60)[0]

        totalHour, totalMinute = divmod(totalMinute, 60)

        # Possibility 1: Multiple hours left.
        if ((totalMinute % 60) == 0) and (totalMinute != 60):
            displayDescription = (f"You have **{totalHour} hours** left.")

        # Possibility 2: 1 hour left.
        elif (totalMinute == 60):
            displayDescription = (f"You have **{totalHour} hour** left.")

        # Possibility 3: Multiple hours and multiple minutes left.
        elif (totalHour > 1) and (totalMinute > 1):
            displayDescription = (
                f"You have **{totalHour} hours** and **{totalMinute} minutes** left.")

        # Possibility 4: 1 hour and multiple minutes left.
        elif (totalHour == 1) and (totalMinute > 1):
            displayDescription = (
                f"You have **{totalHour} hour** and **{totalMinute} minutes** left.")

        # Possibility 5: Multiple hours and one minute left.
        elif (totalHour > 1) and (totalMinute == 1):
            displayDescription = (
                f"You have **{totalHour} hours** and **{totalMinute} minute** left.")

        # Possibility 6: One hour and one minute left.
        elif (totalHour == 1) and (totalMinute == 1):
            displayDescription = (
                f"You have **{totalHour} hour** and **{totalMinute} minute** left.")

        # Possibility 7: Multiple minutes left.
        elif (totalHour < 1) and (totalMinute > 1):
            displayDescription = (f"You have ** {totalMinute} minutes** left.")

        # Possibility 8: Less then a minute left.
        elif (totalHour < 1) and (totalMinute == 1):
            displayDescription = (f"You have less then a **minute** left.")

        return displayDescription


def setup(bot):
    bot.add_cog(UserInterface(bot))
