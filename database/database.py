import os
import json
from pymongo import MongoClient
from nextcord.ext import commands

# Checks if the database JSON file exists and loads it
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as x:
        configData = json.load(x)

    cluster = MongoClient(configData["DATABASEPASSWORD"])
    db = cluster["DinoBot"]
    collection = db["studyData"]

else:
    print("Database is NOT connected!")

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def databaseInsertion(userIdentity, timeStudied):
        
        #Checking if the user exists
        check = collection.find_one({"_id": userIdentity})
        
        #If no user is in the database we must add them
        if check is None:
            document = {"_id": userIdentity, "studyTime": timeStudied}
            collection.insert_one(document)
        
        #If the user is in the database we must add to the exisiting value
        else:
            result = collection.find_one({"_id": userIdentity}, {"_id": 0, "studyTime": 1})
            updatedAmountStudied = result["studyTime"] + timeStudied
            newResult = {"$set": {"studyTime": updatedAmountStudied}}
            collection.update_one(result, newResult)

    async def databaseReceiving(userIdentity):
        result = collection.find_one({"_id": userIdentity}, {"_id": 0, "studyTime": 1})

        try:
            return(result["studyTime"])
        
        except (TypeError):
            #If the user has never studied before we cant return anything
            return 0

def setup(bot):
    bot.add_cog(Database(bot))
