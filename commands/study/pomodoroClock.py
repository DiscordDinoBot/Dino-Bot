import nextcord, math, time, asyncio
from nextcord import ButtonStyle
from nextcord.ui import Button, View
from nextcord.ext import commands


class PomodoroClock(commands.Cog):
  
  def __init__(self, bot):
    
    PomodoroClock.bot = bot

    studyDictionary = {}
    breakDictionary = {}
    longBreakDictionary = {}
    sessionState = {}
    pauseState = {}
    finishState = {}

    PomodoroClock.studyDictionary = studyDictionary
    PomodoroClock.breakDictionary = breakDictionary
    PomodoroClock.longBreakDictionary = longBreakDictionary
    PomodoroClock.sessionState = sessionState
    PomodoroClock.pauseState = pauseState
    PomodoroClock.finishState = finishState


  
  async def setPomodoro(self, studyTime, breakTime, longBreakTime, userIdentity):
    
    PomodoroClock.studyDictionary[userIdentity] = studyTime
    PomodoroClock.breakDictionary[userIdentity] = breakTime
    PomodoroClock.longBreakDictionary[userIdentity] = longBreakTime
    PomodoroClock.sessionState[userIdentity] = 0
    PomodoroClock.pauseState[userIdentity] = False
    PomodoroClock.finishState[userIdentity] = False

  
  
  async def setButtons(self):
        
    finishButton = Button(label="Finish", style = ButtonStyle.green)
    pauseButton = Button(label="Pause", style = ButtonStyle.red)
    skipButton = Button(label="Skip", style = ButtonStyle.blurple)
    resumeButton = Button(label="Resume", style = ButtonStyle.green)
    
    #Button View for any active sessions.
    self.activeSessionButtons = View() 
    self.activeSessionButtons.add_item(finishButton) 
    self.activeSessionButtons.add_item(pauseButton) 
    self.activeSessionButtons.add_item(skipButton)
  
    #Button View for any paused sessions.
    self.pausedSessionButtons = View()
    self.pausedSessionButtons.add_item(resumeButton)
    
    #Response functions.
    finishButton.callback = PomodoroClock.responseFinishButton
    pauseButton.callback = PomodoroClock.responsePauseButton
    skipButton.callback = PomodoroClock.responseSkipButton
    resumeButton.callback = PomodoroClock.responseResumeButton


  
  async def setSessionState(self, userIdentity):
    if (PomodoroClock.sessionState[userIdentity]) == 7:
      PomodoroClock.sessionState[userIdentity] = 0

    else:
      PomodoroClock.sessionState[userIdentity] += 1



  async def getDisplayTitle(self, userIdentity):
    if (PomodoroClock.sessionState[userIdentity]) == 7:
      displayTitle = "Long Break"
      
    elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
      displayTitle = "Break"
      
    elif(PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
      displayTitle = "Study"

    return displayTitle


  
  async def getDisplayDescription(self, remainingSeconds):

    totalMinute = math.ceil(remainingSeconds / 60)
    
    totalHour = math.trunc(totalMinute / 60)

    #Possibility 1: Multiple hours left.
    if ((totalMinute % 60) == 0) and (totalMinute != 60):
      displayDescription = (f"You have **{totalHour} hours** left.")
    
    #Possibility 2: 1 hour left.
    elif (totalMinute == 60):
      displayDescription = (f"You have **{totalHour} hour** left.")
    
    #Possibility 3: Multiple hours and multiple minutes left.
    elif (totalHour > 1) and (totalMinute > 1):
      displayDescription = (f"You have **{totalHour} hours** and **{totalMinute} minutes** left.") 
  
    #Possibility 4: 1 hour and multiple minutes left.
    elif (totalHour == 1) and (totalMinute > 1):
      displayDescription = (f"You have **{totalHour} hour** and **{totalMinute} minutes** left.")   
  
    #Possibility 5: Multiple hours and one minute left.
    elif (totalHour > 1) and (totalMinute == 1):
      displayDescription = (f"You have **{totalHour} hours** and **{totalMinute} minute** left.")
  
    #Possibility 6: One hour and one minute left.
    elif (totalHour == 1) and (totalMinute == 1):
      displayDescription = (f"You have **{totalHour} hour** and **{totalMinute} minute** left.")
    
    #Possibility 7: Multiple minutes left.
    elif (totalHour < 1) and (totalMinute > 1):
      displayDescription = (f"You have ** {totalMinute} minutes** left.")
    
    #Possibility 8: Less then a minute left.
    elif (totalHour < 1) and (totalMinute == 1):
      displayDescription = (f"You have less then a **minute** left.")
  
    return displayDescription


  
  async def getDisplayColour(self, userIdentity):
    if (PomodoroClock.sessionState[userIdentity] == 7):
      red = 8
      green = 54
      blue = 133
      
    elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
      red = 61
      green = 53
      blue = 102
      
    elif(PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
      red = 255
      green = blue = 66
    
    return red, green, blue
    

  
  async def getSessionState(self, userIdentity):
    return PomodoroClock.sessionState[userIdentity]
  

  
  async def getStudyTime(self, userIdentity):
    return PomodoroClock.studyDictionary[userIdentity]
  
  

  async def getBreakTime(self, userIdentity):
    return PomodoroClock.breakDictionary[userIdentity]
  


  async def getLongBreakTime(self, userIdentity):
    return PomodoroClock.longBreakDictionary[userIdentity]



  async def responseFinishButton(self):
    print("You pressed the Finish button.")


  
  async def responsePauseButton(self):
    PomodoroClock.pauseState[self.user.id] = True
    print(PomodoroClock.pauseState)
    print("Done")


  
  async def responseSkipButton(self):
    print("You pressed the Skip button.")


  
  async def responseResumeButton(self):
    print("You pressed the Resume button.")


  
  async def controlPomodoro(self, ctx, userIdentity):
    #Checks if user has paused the session
    if (PomodoroClock.pauseState[userIdentity] == True):
      await PomodoroClock.pausePomodoro(self, ctx, userIdentity)


    #Checks if user has finished the session
    elif (PomodoroClock.finishState[userIdentity] == True):
      await PomodoroClock.finishPomodoro(self, ctx, userIdentity)
    

    #Checks if the user wants to run a study session
    elif (PomodoroClock.sessionState[userIdentity]) in (0, 2, 4, 6):
      timeSeconds = await PomodoroClock.getStudyTime(self, userIdentity)
      await PomodoroClock.clockPomodoro(self, ctx, userIdentity, timeSeconds)
    

    #Checks if user wants to run a break session
    elif (PomodoroClock.sessionState[userIdentity]) in (1, 3, 5):
      timeSeconds = await PomodoroClock.getBreakTime(self, userIdentity)
      await PomodoroClock.clockPomodoro(self, ctx, userIdentity, timeSeconds)


    #Checks if user wants to run a long break session
    elif (PomodoroClock.sessionState[userIdentity]) == 7:
      timeSeconds = await PomodoroClock.getLongBreakTime(self, userIdentity)
      await PomodoroClock.clockPomodoro(self, ctx, userIdentity, timeSeconds)

  


  async def clockPomodoro(self, ctx, userIdentity, timeSeconds):
    #Gets all the information for the initial display message
    red, green, blue = await PomodoroClock.getDisplayColour(self, userIdentity) 
    displayTitle = await PomodoroClock.getDisplayTitle(self, userIdentity)
    displayDescription = await PomodoroClock.getDisplayDescription(self, timeSeconds)
    
    #Sets the initial embed message with the variables we recieved above
    embed = nextcord.Embed(title = (f"{displayTitle} Session"), description = (displayDescription), colour = nextcord.Colour.from_rgb(red, green, blue))
    #Sends the initial display message and assigns it to a variable so we can edit it in the next loop
    displayMessage = await ctx.send(view=self.activeSessionButtons, embed=embed)

    whileStartTime = time.time()
    
    while (timeSeconds > 0):
  
      loopStartTime = time.time()
      
      if ((timeSeconds % 60) == 0):
        red, green, blue = await PomodoroClock.getDisplayColour(self, userIdentity) 
        displayTitle = await PomodoroClock.getDisplayTitle(self, userIdentity)
        displayDescription = await PomodoroClock.getDisplayDescription(self, timeSeconds)
        
        embed = nextcord.Embed(title = (f"{displayTitle} Session"), description = (displayDescription), colour = nextcord.Colour.from_rgb(red, green, blue))
        await displayMessage.edit(view=self.activeSessionButtons, embed=embed)
      
      timeSeconds -= 1
        
      loopEndTime = time.time()
      await asyncio.sleep(1 - (loopEndTime - loopStartTime))

    whileEndTime = time.time()
    print(whileEndTime - whileStartTime)

    await displayMessage.delete()

    if (timeSeconds <= 0):
      await PomodoroClock.setSessionState(self, userIdentity)
    
    await PomodoroClock.controlPomodoro(self, ctx, userIdentity)



  async def pausePomodoro(self, ctx, userIdentity):
    await ctx.send(f"This is the paused message for {userIdentity}")



  async def finishPomodoro(self, ctx, userIdentity):
    await ctx.send(f"You have finished your Pomodoro session for {userIdentity}")



  async def runPomodoro(self, ctx, userIdentity):
    await self.setButtons()
    await self.controlPomodoro(ctx, userIdentity)
  
             
#Setup function
def setup(bot):
  bot.add_cog(PomodoroClock(bot))