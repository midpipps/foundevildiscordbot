import discord
import requests
import logging
import sqlite3
import os

import config
from plugins import PluginInterface


class Scoreboard(PluginInterface):
    '''
    The scoreboard system for foundevilbot
    '''
    def setupdb(self):
        with sqlite3.connect(os.path.join(config.DB_FOLDER, config.META_DB)) as conn:
            c = conn.cursor()
            tablecreatesql = '''
                                CREATE TABLE IF NOT EXISTS antisiphon (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    overall_place INTEGER NOT NULL,
                                    relative_place INTEGER NOT NULL,
                                    team_id INTEGER NOT NULL,
                                    challenges_solved INTEGER NOT NULL,
                                    acet_level INTEGER NOT NULL,
                                    last_solution INTEGER
                                );
                            '''
            c.executescript(tablecreatesql)
    
    def updatedb(self, website) -> str:
        '''
        Compare the database to the 
        '''
        outputstring = ""
        with sqlite3.connect(os.path.join(config.DB_FOLDER, config.META_DB)) as conn:
            c = conn.cursor()
            sqlquery = "SELECT id, username, overall_place, relative_place, team_id, challenges_solved, acet_level, last_solution FROM antisiphon where username = :username;"
            c.execute(sqlquery, website)
            databasedata = c.fetchone()
            if databasedata:
                if databasedata[2] != website.get("overall_place"):
                    movement = databasedata[2] - website.get("overall_place")
                    outputstring += "{0} moved {1} places {2}\n".format(website.get('username'), movement, "Congratulations" if movement > 0 else "keep working you got this")
                if databasedata[3] != website.get("relative_place"):
                    movement =  databasedata[3] - website.get("relative_place")
                    outputstring += "{0} moved {1} places compared to the rest of you {2}\n".format(website.get('username'), movement, "Congratulations" if movement > 0 else "keep working you got this")
                if databasedata[5] != website.get("challenges_solved"):
                    movement = website.get("challenges_solved") - databasedata[5]
                    outputstring += "{0} solved {1} more items you rock\n".format(website.get('username'), movement)
                if databasedata[6] != website.get("acet_level"):
                    movement = website.get("acet_level") - databasedata[6]
                    outputstring += "{0} moved {1} ACET levels and is now {2}\n".format(website.get('username'), movement, website.get("acet_level"))
                sql_query = '''
                            UPDATE antisiphon SET
                            overall_place=:overall_place,
                            relative_place=:relative_place,
                            team_id=:team_id,
                            challenges_solved=:challenges_solved,
                            acet_level=:acet_level,
                            last_solution=:last_solution
                            WHERE
                            username = :username;
                            '''
                c.execute(sql_query, website)
            else:
                outputstring = "Welcome to the game {0}\n".format(website.get('username'))
                sql_query = '''
                            INSERT INTO antisiphon
                            (username, overall_place, relative_place, team_id, challenges_solved, acet_level, last_solution)
                            VALUES
                            (:username, :overall_place, :relative_place, :team_id, :challenges_solved, :acet_level, :last_solution)
                            '''
                c.execute(sql_query, website)
        
        return outputstring
    def getscoreboardupdate(self):
        temp = requests.get(config.META_CTF_URL)
        jsondata = temp.json()
        updatestring = ""
        outstring = "```\n"
        outstring += "{0:>5} {1:>7} {3:>7}   {2:18} \n".format("NDIT","Overall","Username","Score")
        for entry in jsondata:
            outstring += "{relative_place:5} {overall_place:7} {score:7}   {username:18}\n".format(**entry)
            updatestring += self.updatedb(entry)
        outstring += "\n\n" + updatestring
        outstring += "```"
        return outstring

    def handles(self, message:discord.Message) -> bool:
        '''
        Should return true if it handles the message otherwise false
        '''
        return message.content.lower().startswith('/scoreboard')

    async def on_message(self, message:discord.Message):
        '''
        called when a new message is received will return the scoreboard and other stats
        '''
        if self.handles(message):
            logging.getLogger('discord').info('Message from {0.author.display_name}: {0.content} SCOREBOARD Picked it up'.format(message))
            #TROLL_IDS in Config\Example_init_.py is empty. So this is next best thing...
            #if message.author.discriminator in config.TROLL_IDS:
            #    logging.getLogger('discord').info('{0} asked so TROLLOLOL'.format(message.author.display_name))
            #    await message.channel.send("You are Number 1 in our hearts.")
            #else:
            logging.getLogger('discord').info('{0} asked for scoreboard'.format(message.author.display_name))
            await message.channel.send(self.getscoreboardupdate())
    
    def min_help(self) -> str:
        '''
        minimal help text for listing with all other help text
        '''
        return "/scoreboard - displays the current scoreboard that is being watched"
    
    def specific_help(self, command:str) -> str:
        '''
        bool to cover help message to this classes specific function
        return true if you are handling this help false otherwise
        '''
        if command.lower().startswith("scoreboard"):
            return "```/scoreboard has no options and only does one thing which is returns the darn data```"
        return None

    def init(self) -> None:
        '''
        Initialize all the stuff that we need for this feature to work
        '''
        self.setupdb();
