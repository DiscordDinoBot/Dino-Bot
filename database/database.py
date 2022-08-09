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

    async def allTimeStatistics(userIdentity):
        allTimeData = allTimeCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "studyTime": 1})

        # Checks if the user has studied before.
        if (allTimeData is None):
            return 0

        # If the user has studied then the amount of time is returned.
        else:
            return((allTimeCollection.find_one({"_id": userIdentity}, {"_id": 0, "studyTime": 1}))["studyTime"])

    async def yearStatistics(userIdentity):
        yearData = yearCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "year": 1})

        #Checks if the user has studied in the past year.
        if (yearData is None) or ((yearData["year"]) != (int((datetime.datetime.now()).strftime("%Y")))):
            return 0

        #Returns the amount of time the user has studied.
        else:
            return((yearCollection.find_one({"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1}))["yearStudyTime"])

    async def yearValidation(userIdentity):
        yearData = yearCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "year": 1})

        if yearData is None:
            pass

        elif ((yearData["year"]) != (int((datetime.datetime.now()).strftime("%Y")))):
            yearCollection.delete_one(yearData)

    async def allTimeInsertion(userIdentity, timeStudied):

        # Checking if the user exists
        collection = allTimeCollection.find_one({"_id": userIdentity})

        # If no user is in the database we must add them
        if collection is None:
            document = {"_id": userIdentity, "studyTime": timeStudied}
            allTimeCollection.insert_one(document)

        # If the user is in the database we must add to the exisiting value
        else:
            result = allTimeCollection.find_one(
                {"_id": userIdentity}, {"_id": 0, "studyTime": 1})
            updatedAmountStudied = result["studyTime"] + timeStudied
            newResult = {"$set": {"studyTime": updatedAmountStudied}}
            allTimeCollection.update_one(result, newResult)

    async def yearInsertion(userIdentity, timeStudied):

        await Database.yearValidation(userIdentity)

        collection = yearCollection.find_one({"_id": userIdentity})
        year = int((datetime.datetime.now()).strftime("%Y"))

        if collection == None:
            document = {"_id": userIdentity,
                        "yearStudyTime": timeStudied, "year": year}
            yearCollection.insert_one(document)

        else:
            result = yearCollection.find_one(
                {"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1})
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

        allTime = await Database.allTimeStatistics(userIdentity)
        yearTime = await Database.yearStatistics(userIdentity)

        return allTime, yearTime


def setup(bot):
    bot.add_cog(Database(bot))
