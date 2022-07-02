import nextcord
from nextcord.ext import commands

from .pomodoroClock import PomodoroClock

#Class that takes in the input from Selection Menu for the bot.
class PomodoroInput(commands.Cog):
  def __init__(self, bot):
    
    PomodoroInput.bot = bot
    PomodoroInput.pomodoroClockFile = PomodoroClock(bot)

    sessionActive = {}
    selectionMenuActive = {}

    PomodoroInput.sessionActive = sessionActive
    PomodoroInput.selectionMenuActive = selectionMenuActive
  
  #Study command that will run the Selection Menu.
  @commands.command()
  async def study(self, ctx):

    #If the user is in an active session, we will stop the function from continuing.
    if ctx.author.id in PomodoroInput.sessionActive:
      if PomodoroInput.sessionActive[ctx.author.id] == True:
        await ctx.author.send("You currently have an active session. Please finish that one before starting another.")
        return
    
    PomodoroInput.sessionActive[ctx.author.id] = True
    PomodoroInput.selectionMenuActive[ctx.author.id] = True

    PomodoroInput.selectionMenuMessage = await ctx.send("Choose a selection menu!" , view = DropdownView())


#Inner class that will run the view for the menu.
class DropdownView(nextcord.ui.View):
  @nextcord.ui.select(

    placeholder='Select a studying time.', 
    min_values=1, 
    max_values=1,
    
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
  )

  #This is the callback function that will run once the selection has been made from the user.
  async def callback(self, select, interaction: nextcord.Interaction):
    
    PomodoroInput.selectionMenuActive[interaction.user.id] = False

    '''
    All the following variables are in seconds.

    pomodoroTime is the study time.
    shortBreak is the short break time.
    longBreak is the long break time.
    '''
    
    #Beginner is selected.
    if (select.values[0] == "Beginner"):
      pomodoroTime = 2
      shortBreak = 5
      longBreak = 10

    #Intermediate is selected.
    elif (select.values[0] == "Intermediate"):
      pomodoroTime = 1500
      shortBreak = 300
      longBreak = 900
        
    #Expert is selected.
    elif (select.values[0] == "Expert"):
      pomodoroTime = 2700
      shortBreak = 300
      longBreak = 1200
      
    #Regular is selected.
    elif (select.values[0] == "Regular"):
      pomodoroTime = 1500
      shortBreak = 300
      longBreak = 900
    
    #Custom is selected.
    elif (select.values[0] == "Custom"):

      '''
      Nothing in here yet. Planning on putting another selection menu
      that the user can use to select custom times for the session.

      Currently this will remove the user id from the active list so the user is not
      locked out of making another session
      '''

      PomodoroInput.sessionActive[interaction.user.id] = False
      PomodoroInput.selectionMenuActive[interaction.user.id] = False
      
      #This are currently here so the function stops. Remove them once the custom menu is made.
      await PomodoroInput.selectionMenuMessage.delete()
      await interaction.send("**Custom** is currently in development. Please pick another option.")
      return

    if PomodoroInput.selectionMenuActive[interaction.user.id] == False:
      #Deletes the selection menu once the option has been choosed.
      await PomodoroInput.selectionMenuMessage.delete()
      pass
          
    #This will run the cancel selection for the menu.
    if (select.values[0] == 'Cancel'):
      #Runs the verifcation function that will remove the user from the active list
      PomodoroInput.sessionActive[interaction.user.id] = False
      PomodoroInput.selectionMenuActive[interaction.user.id] = False
    
    #Redirects any other selections to the control file.
    else:
      await PomodoroInput.pomodoroClockFile.setPomodoro(pomodoroTime, shortBreak, longBreak, interaction.user.id)
      await PomodoroInput.pomodoroClockFile.runPomodoro(interaction.user, interaction.user.id)


#Setup function.
def setup(bot):
  bot.add_cog(PomodoroInput(bot))