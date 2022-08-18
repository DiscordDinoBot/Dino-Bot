import os
import json
import datetime
import pytz
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
        Database.pst = pytz.timezone('America/Los_Angeles')

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

        # Checks if the user has studied in the past year.
        if (yearData is None) or ((yearData["year"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y")))):
            return 0

        # Returns the amount of time the user has studied in the year.
        else:
            return((yearCollection.find_one({"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1}))["yearStudyTime"])

    async def monthStatistics(userIdentity):
        monthData = monthCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "yearMonth": 1})

        # Checks if the user has studied in the past month.
        if (monthData is None) or ((monthData["yearMonth"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y%m")))):
            return 0

        # Returns the amount of time the user has studied in the month.
        else:
            return((monthCollection.find_one({"_id": userIdentity}, {"_id": 0, "monthStudyTime": 1}))["monthStudyTime"])

    async def dailyStatistics(userIdentity):
        dailyData = dailyCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "yearMonthDay": 1})

        # Checks if the user has studied in the past day.
        if (dailyData is None) or ((dailyData["yearMonthDay"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y%m%d")))):
            return 0

        # Returns the amount of time the user has studied in the day.
        else:
            return((dailyCollection.find_one({"_id": userIdentity}, {"_id": 0, "dailyStudyTime": 1}))["dailyStudyTime"])

    async def yearValidation(userIdentity):
        yearData = yearCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "year": 1})

        # Checks if the user has studied in the year.
        if yearData is None:
            pass

        # Checks if the year is outdated and will delete it from the database.
        elif ((yearData["year"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y")))):
            yearCollection.delete_one(yearData)

    async def monthValidation(userIdentity):
        monthData = monthCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "yearMonth": 1})

        # Checks if the user has studied in the month.
        if monthData is None:
            pass

        # Checks if the month is outdated and will delete it from the database.
        elif ((monthData["yearMonth"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y%m")))):
            monthCollection.delete_one(monthData)
    
    async def dailyValidation(userIdentity):
        dailyData = dailyCollection.find_one(
            {"_id": userIdentity}, {"_id": 0, "yearMonthDay": 1})

        # Checks if the user has studied in the day.
        if dailyData is None:
            pass

        # Checks if the day is outdated and will delete it from the database.
        elif ((dailyData["yearMonthDay"]) != (int((datetime.datetime.now(Database.pst)).strftime("%Y%m%d")))):
            dailyCollection.delete_one(dailyData)

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

        # Checks that the year is valid.
        await Database.yearValidation(userIdentity)

        collection = yearCollection.find_one({"_id": userIdentity})
        # Getting current year.
        year = int((datetime.datetime.now(Database.pst)).strftime("%Y"))

        # Checks if the document is empty. If it is empty then we add a document for it.
        if collection == None:
            document = {"_id": userIdentity,
                        "yearStudyTime": timeStudied, "year": year}
            yearCollection.insert_one(document)

        # Document exists.
        else:
            result = yearCollection.find_one(
                {"_id": userIdentity}, {"_id": 0, "yearStudyTime": 1})

            # Calculates new total amount studied.
            updatedAmountStudied = result["yearStudyTime"] + timeStudied

            # Updates the new amount studied.
            newResult = {"$set": {"yearStudyTime": updatedAmountStudied}}
            yearCollection.update_one(result, newResult)

    async def monthInsertion(userIdentity, timeStudied):
        await Database.monthValidation(userIdentity)

        collection = monthCollection.find_one({"_id": userIdentity})

        #Gets current month and year from the date time (Ex: 202208)
        yearMonth = int((datetime.datetime.now(Database.pst)).strftime("%Y%m"))

        if collection == None:
            document = {"_id": userIdentity,
                        "monthStudyTime": timeStudied, "yearMonth": yearMonth}
            monthCollection.insert_one(document)

        # Document exists.
        else:
            result = monthCollection.find_one(
                {"_id": userIdentity}, {"_id": 0, "monthStudyTime": 1})
            # Calculates new total amount studied.    
            updatedAmountStudied = result["monthStudyTime"] + timeStudied
            # Updates the new amount studied.
            newResult = {"$set": {"monthStudyTime": updatedAmountStudied}}
            monthCollection.update_one(result, newResult)
            
    async def dailyInsertion(userIdentity, timeStudied):
        await Database.dailyValidation(userIdentity)

        collection = dailyCollection.find_one({"_id": userIdentity})

        #Gets current day, month and year from the date time (Ex: 20220811)
        yearMonthDay = int((datetime.datetime.now(Database.pst)).strftime("%Y%m%d"))

        if collection == None:
            document = {"_id": userIdentity,
                        "dailyStudyTime": timeStudied, "yearMonthDay": yearMonthDay}
            dailyCollection.insert_one(document)

        # Document exists.
        else:
            result = dailyCollection.find_one(
                {"_id": userIdentity}, {"_id": 0, "dailyStudyTime": 1})
            # Calculates new total amount studied.    
            updatedAmountStudied = result["dailyStudyTime"] + timeStudied
            # Updates the new amount studied.
            newResult = {"$set": {"dailyStudyTime": updatedAmountStudied}}
            dailyCollection.update_one(result, newResult)

    async def databaseControl(userIdentity, timeStudied):
        await Database.allTimeInsertion(userIdentity, timeStudied)
        await Database.yearInsertion(userIdentity, timeStudied)
        await Database.monthInsertion(userIdentity, timeStudied)
        await Database.dailyInsertion(userIdentity, timeStudied)

    async def databaseReceiving(userIdentity):

        allTime = await Database.allTimeStatistics(userIdentity)
        yearTime = await Database.yearStatistics(userIdentity)
        monthTime = await Database.monthStatistics(userIdentity)
        dailyTime = await Database.dailyStatistics(userIdentity)

        return allTime, yearTime, monthTime, dailyTime


def setup(bot):
    bot.add_cog(Database(bot))
