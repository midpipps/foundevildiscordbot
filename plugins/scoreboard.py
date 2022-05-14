import discord
import requests
import logging

import config
from plugins import PluginInterface


class Scoreboard(PluginInterface):
    '''
    The scoreboard system for foundevilbot
    '''

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
            if message.author.discriminator in config.TROLL_IDS:
                logging.getLogger('discord').info('{0} asked so TROLLOLOL'.format(message.author.display_name))
                await message.channel.send("You are Number 1 in our hearts.")
            else:
                logging.getLogger('discord').info('{0} asked for scoreboard'.format(message.author.display_name))
                temp = requests.get(config.META_CTF_URL)
                jsondata = temp.json()
                outstring = "```\n"
                outstring += "{0:>5} {1:>7} {3:>7}   {2:18} \n".format("NDIT","Overall","Username","Score")
                for entry in jsondata:
                    outstring += "{relative_place:5} {overall_place:7} {score:7}   {username:18}\n".format(**entry)
                outstring += "```"
                await message.channel.send(outstring)
    
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