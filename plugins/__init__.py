from sys import implementation
import asyncio
import discord

class PluginInterface(object):
    '''
    The interface for foundevilbot to make new repliers
    '''
    def handles(self, message:discord.Message) -> bool:
        '''
        Should return true if it handles the message otherwise false
        '''
        raise NotImplementedError("handles has not been defined yet")

    async def on_message(self, message:discord.Message):
        '''
        called when a new message is received if handled message return true else return false
        '''
        raise NotImplementedError("On Message has not been defined yet")
    
    def min_help(self) -> str:
        '''
        minimal help text for listing with all other help text
        '''
        raise NotImplementedError("min_help not defined yet")

    def specific_help(self, command:str) -> str:
        '''
        bool to cover help message to this classes specific function
        return helptext if you are handling this help None otherwise
        '''
        raise NotImplementedError("specific_help has not been defined yet")