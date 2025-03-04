import discord
from discord.ext import commands, tasks
from colorama import Fore, Style
import asyncio
from dotenv import load_dotenv
import os

#loads config file
load_dotenv(os.path.join(os.path.dirname(__file__),"Config.env"))

botPrefix = os.getenv("BotPrefix")

bot = commands.Bot(command_prefix=[botPrefix.upper(),botPrefix.lower()], intents=discord.Intents.all())
bot.remove_command('help') #Removes default help command

@bot.event
async def on_ready():
    print(Fore.YELLOW +f"[-----------------------]\nRoBot Ready\n[-----------------------]"+Style.RESET_ALL)
    checkVC.start()


lastCheckMembers = []

@tasks.loop(seconds=5)
async def checkVC():
    global lastCheckMembers
    channel = bot.get_channel(int(os.getenv("MonitoredChannel"))) #gets the channel you want to get the list from | Needs to take a channel ID

    connectedMembers = channel.members #finds members connected to the channel
    connectedMembersID = [member.id for member in connectedMembers]

    joinedMembers = []
    leftMembers = []
    


    for member in connectedMembersID:
        if len(connectedMembersID) > 0:
            if member not in lastCheckMembers:
                joinedMembers.append(member)

    for member in lastCheckMembers:
        if len(lastCheckMembers) > 0:
            if member not in connectedMembersID:
                leftMembers.append(member)


    

    print(f"{joinedMembers} \\ {leftMembers}")

    announceChannel = bot.get_channel(int(os.getenv("SendChannel")))

    if len(joinedMembers) > 0:
        for id in joinedMembers:
            await announceChannel.send(f"<@>, <@{id}> has joined the call")

    if len(leftMembers) > 0:
        for id in leftMembers:
            await announceChannel.send(f"<@>, <@{id}> has left the call")

    joinedMembers.clear()
    leftMembers.clear()

    lastCheckMembers = connectedMembersID

    
@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")


#Loads bot token
load_dotenv(os.path.join(os.path.dirname(__file__),"API_Token.env"))

bot.run(os.getenv("API_TOKEN"))
