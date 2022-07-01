from nextcord.ext import commands

#Class that is used to verify if the user has an active session
class PomodoroVerification (commands.Cog):

  #Sets the initial list for the activeUsers
  #**ONLY RUNS ON START-UP**
  activeUsers = [] 
  
  def __init__(self, bot):
    self.bot = bot
  
  #Function that checks if the user is in the active list
  async def pomodoroVerificationCheck(self, pomodoroUser):
    #User is an active user
    if pomodoroUser in (PomodoroVerification.activeUsers):
      print(PomodoroVerification.activeUsers)
      return False

    #User is not an active user
    else:
      #Adds the user ID into the active list
      PomodoroVerification.activeUsers.append(pomodoroUser)
      print(PomodoroVerification.activeUsers)
      return True

  #Function that can modify the active user list 
  async def pomodoroVerificationRemove(self, pomodoroUser):
    #Checks if the user is in the active list to prevent error.
    if pomodoroUser in (PomodoroVerification.activeUsers):
      PomodoroVerification.activeUsers.remove(pomodoroUser)
      print("Working")
      print(PomodoroVerification.activeUsers)
      return
    
    print("Error! User not removed...")

def setup(bot):
  bot.add_cog(PomodoroVerification(bot))