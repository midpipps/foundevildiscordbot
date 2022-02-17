import logging
import logging.handlers
import os
import discord
import config
import plugins.scoreboard
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(config.LOG_LEVEL)
handler = logging.handlers.RotatingFileHandler(filename=os.path.join(config.LOG_DIRECTORY, config.LOG_FILENAME), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

PLUGINLIST = [plugins.scoreboard.Scoreboard()]

class FoundEvilTheBot(discord.Client):
    async def on_ready(self):
        logger.info('Logged on as {name}!'.format(name=self.user.display_name))

    async def on_message(self, message:discord.Message):
        if message.content.startswith("/"):
            if message.content.lower() == ('/fetbhelp') or message.content.lower() == ('/fetb'):
                logger.info('Command from {0.author.display_name}: {0.content}'.format(message))
                outputstring = "```\nFound Evil The Bot Commands use /fetbhelp or /fetb <plugincommand> for information on any command\n"
                for entry in PLUGINLIST:
                    outputstring += entry.min_help() + "\n"
                outputstring += "```"
                await message.channel.send(outputstring)
            elif message.content.lower().startswith('/fetbhelp') or message.content.lower().startswith('/fetb'):
                for entry in PLUGINLIST:
                    result = entry.specific_help(message.content.split(' ', 1)[1])
                    if result:
                        await message.channel.send(result)
            elif message.content.lower() == ('/goodbot'):
                await message.channel.send("Aw shucks thank you.")
            else:
                for entry in PLUGINLIST:
                    if entry.handles(message):
                        await entry.on_message(message)
                        break


client = FoundEvilTheBot()
client.run(config.DISCORD_API_TOKEN)

