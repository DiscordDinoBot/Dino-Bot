import os
import json
import datetime
from pymongo import MongoClient
from nextcord.ext import commands

# Checks if the database JSON file exists and loads it
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as x:
        configData = json.load(x)

    cluster = MongoClient(configData["DATABASEPASSWORD"])
    db = cluster["DinoBot"]
    allTimeCollection = db["studyData"]
    yearCollection = db["studyDataYear"]
    monthCollection = db["studyDataMonth"]
    dailyCollection = db["studyDataDaily"]

else:
    print("Database is NOT connected!")

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def allTimeInsertion(userIdentity, timeStudied):
        
        #Checking if the user exists
        collection = allTimeCollection.find_one({"_id": userIdentity})
        
        #If no user is in the database we must add them
        if collection is None:
            document = {"_id": userIdentity, "studyTime": timeStudied}
            allTimeCollection.insert_one(document)
        
        #If the user is in the database we must add to the exisiting value
        else:
            result = allTimeCollection.find_one({"_id": userIdentity}, {"_id": 0, "studyTime": 1})
            updatedAmountStudied = result["studyTime"] + timeStudied
            newResult = {"$set": {"studyTime": updatedAmountStudied}}
            allTimeCollection.update_one(result, newResult)
    
    async def yearInsertion(userIdentity, timeStudied):

        collection = yearCollection.find_one({"_id": userIdentity})
        date = datetime.datetime.now()
        year = int(date.strftime("%Y"))

        result = yearCollection.find_one({"_id": userIdentity}, {"_id": 0, "year": 1})
        databaseYear = result["year"]


        if collection is None or (databaseYear != year):
            document = {"_id": userIdentity, "yearStudyTime": timeStudied, "year": year}
            yearCollection.insert_one(document)

        else:
            result = yearCollection.find_one({"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1})
            updatedAmountStudied = result["yearStudyTime"] + timeStudied
            newResult = {"$set": {"yearStudyTime": updatedAmountStudied}}
            yearCollection.update_one(result, newResult)

    async def monthInsertion(userIdentity, timeStudied):
        pass

    async def dailyInsertion(userIdentity, timeStudied):
        pass

    async def databaseControl(userIdentity, timeStudied):
        await Database.allTimeInsertion(userIdentity, timeStudied)
        await Database.yearInsertion(userIdentity, timeStudied)
        await Database.monthInsertion(userIdentity, timeStudied)
        await Database.dailyInsertion(userIdentity, timeStudied)
    
    async def databaseReceiving(userIdentity):


        #WRITE A FUNCTION THAT WILL CLEAR ANY OLD DATA ENTRIES OR
        #SET THE MESSAGES TO EXPIRE INSTEAD


        allTime = allTimeCollection.find_one({"_id": userIdentity}, {"_id": 0, "studyTime": 1})
        yearTime = yearCollection.find_one({"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1})

        try:
            return(allTime["studyTime"], yearTime["yearStudyTime"])
        
        except (TypeError):
            #If the user has never studied before we cant return anything
            return 0

def setup(bot):
    bot.add_cog(Database(bot))
