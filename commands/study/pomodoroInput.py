import nextcord
from nextcord.ext import commands

from .pomodoroClock import PomodoroClock
from .pomodoroVerification import PomodoroVerification

#Class that takes in the input from Selection Menu for the bot.
class PomodoroInput(commands.Cog):
  def __init__(self, bot):
    
    self.bot = bot
    PomodoroInput.pomodoroVerificationFile = PomodoroVerification(bot)
    PomodoroInput.pomodoroClockFile = PomodoroClock(bot)
    
  #Study command that will run the Selection Menu.
  @commands.command()
  async def study(self, ctx):

    #Running the verification file to check if the user is in an active session.
    verificationStatus = await PomodoroInput.pomodoroVerificationFile.pomodoroVerificationCheck(ctx.author.id)

    #If the user is in an active session, we will stop the function from continuing.
    if (verificationStatus) == False:
      await ctx.author.send("You currently have an active session. Please finish that one before starting another.")
      return  

    #Inner class that will run the view for the menu.
    class DropdownView(nextcord.ui.View):
      def __init__(self):
        super().__init__()
        self.add_item(PomodoroInput.Dropdown())
    
    #Setting the view as the class called "DropdownView()"
    view = DropdownView()
    
    #We set this to a variable so we can delete the message after it has been used.
    #Message that contains the selection menu.
    PomodoroInput.selectionMenuMessage = await ctx.author.send(f"Please choose a selection <@{ctx.author.id}>", view=view)
    
  #Class that contains the content for the select options.
  class Dropdown(nextcord.ui.Select):
    def __init__(self):
  
      options = [
  
          #BEGINNER
  
          nextcord.SelectOption(
              label="Beginner",
              emoji="🟩",
              description="Study: 15 Mins | Break: 5 Mins | Long Break: 15 Mins",
              value = 'Beginner'), 
  
          #INTERMEDIATE
  
          nextcord.SelectOption(
              label="Intermediate", 
              emoji="🟧",
              description="Study: 35 Mins | Break: 5 Mins | Long Break: 15 Mins",
              value = 'Intermediate'),
  
          #EXPERT
  
          nextcord.SelectOption(
              label="Expert", 
              emoji="🟥",
              description="Study: 45 Mins | Break: 5 Mins | Long Break: 20 Mins",
              value = 'Expert'),
  
          #REGULAR
  
          nextcord.SelectOption(
              label="Regular", 
              emoji="⬜",
              description="Study: 25 Mins | Break: 5 Mins | Long Break: 15 Mins",
              value = 'Regular'),
  
          #CUSTOM
  
          nextcord.SelectOption(
              label="Custom", 
              emoji="⚙️",
              description="Choose your own times.",
              value = 'Custom'),
    
          #CANCEL
  
          nextcord.SelectOption(
              label="Cancel", 
              emoji="❌",
              value = 'Cancel')
      ]
      #This will be the placeholder and also makes the user only able to choose one of the values. 
      super().__init__(placeholder='Select a studying time.', min_values=1, max_values=1, options=options)

    #This is the callback function that will run once the selection has been made from the user.
    async def callback(self, interaction: nextcord.Interaction):

      '''
      All the following variables are in seconds.

      pomodoroTime is the study time.
      shortBreak is the short break time.
      longBreak is the long break time.
      '''

      #Beginner is selected.
      if (self.values[0] == "Beginner"):
        pomodoroTime = 63
        shortBreak = 30
        longBreak = 900

      #Intermediate is selected.
      elif (self.values[0] == "Intermediate"):
        pomodoroTime = 2100
        shortBreak = 300
        longBreak = 900
           
      #Expert is selected.
      elif (self.values[0] == "Expert"):
        pomodoroTime = 2700
        shortBreak = 300
        longBreak = 1200
        
      #Regular is selected.
      elif (self.values[0] == "Regular"):
        pomodoroTime = 1500
        shortBreak = 300
        longBreak = 900
      
      #Custom is selected.
      elif (self.values[0] == "Custom"):
        '''
        Nothing in here yet. Planning on putting another selection menu
        that the user can use to select custom times for the session.

        Currently this will remove the user id from the active list so the user is not
        locked out of making another session
        '''

        await PomodoroInput.pomodoroVerificationFile.pomodoroVerificationRemove(interaction.user.id)
        
        #This are currently here so the function stops. Remove them once the custom menu is made.
        await PomodoroInput.selectionMenuMessage.delete()
        await interaction.send("**Custom** is currently in development. Please pick another option.")
        return

      
      #Deletes the selection menu once the option has been choosed.
      await PomodoroInput.selectionMenuMessage.delete()
            
      #This will run the cancel selection for the menu.
      if (self.values[0] == 'Cancel'):
        #Runs the verifcation function that will remove the user from the active list
        await PomodoroInput.pomodoroVerificationFile.pomodoroVerificationRemove(interaction.user.id)
      
      #Redirects any other selections to the control file.
      else:
        await PomodoroInput.pomodoroClockFile.setPomodoro(pomodoroTime, shortBreak, longBreak, interaction.user.id, interaction.user.name)
        await PomodoroInput.pomodoroClockFile.runPomodoro(interaction.user, interaction.user.id)

#Setup function.
def setup(bot):
  bot.add_cog(PomodoroInput(bot))