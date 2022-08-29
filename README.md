<img src="https://drive.google.com/uc?export=view&id=1IGTdzN5wzdYgAHxDXg63kbIhXMYNf_7x" width=180 align="right" />
 
# Dino Bot
> Best Discord bot for having focused study sessions.
 
Check out our [website](https://www.dinosaurbot.com) for additional information on the bot!
 
## Project Description
 
Dino Bot is a discord bot that will create study sessions that increase focus. This is acheived by using the Pomodoro Technique. The Technique consists of a 25 minute study session, 5 minute break session and a 15 minute long break session. This is the standard time sessions. You can choose any length of time for your sessions to suit your needs.
 
## Setup
 
1. Use the invite link at [dinosaurbot.com/invite](https://www.dinosaurbot.com/invite).
2. Add the bot to the server.
3. Use **Slash Commands** and start using the bot!
 
## Commands
 
`/study` Initiates the study session and opens the session menu. \
`/stats` Showcases the amount of time the user has studied over various time periods. **(Statistics will be shown in PST Time)**. \
`/timer` Opens a timer that can be used for studying. (**Timer is added to Statistics**). \
`/help` Shows all the commands and additional information.
 
## Documentation
 
This is for anyone who would like to use the code or contribute. Anyone is welcome to contribute code. Code will be approved and merged to production if it is valid and works.
 
#### Installation
 
1. Clone Code from the Repository
2. Install all modules required to run the bot
``pip install nextcord`` and ``pip install pymongo``.
 
3. Run Main.py file. Once this is complete a **config.json** file will be created in your folder.
 
``{"TOKEN": ""`` Insert your bot token into the ``""``
 
``, "DATABASEPASSWORD": ""}`` insert your MongoDB Connection string into the ``""`` \
 
4. You must make 4 collections in your MongoDB database. You can name them the same that the bot uses which would require no change on the code. If you do however change the names then the code for the database is provided in the **database.py**.
\
\
Here is a good [tutorial](https://www.youtube.com/watch?v=rE_bJl2GAY8) that helped me learn how MongoDB works with Python :)
 
## Credits
 
Programming: [Callum Brezden](https://github.com/brezden) \
Contributor: [Wilson Agyapong](https://github.com/WilsoAgya)
 
## License
The source code for the site is licensed under the MIT license, which you can find in the LICENSE.txt file.