import discord
from discord.ext import commands, tasks
from colorama import Fore, Style
import asyncio
from dotenv import load_dotenv
import os




bot = commands.Bot(command_prefix=["R","r"], intents=discord.Intents.all())
bot.remove_command('help') #Removes default help command

@bot.event
async def on_ready():
    print(Fore.YELLOW +f"[-----------------------]\nRoBot Ready\n[-----------------------]"+Style.RESET_ALL)
    checkVC.start()



@tasks.loop(seconds=5)
async def checkVC():
    channel = bot.get_channel() #gets the channel you want to get the list from | Needs to take a channel ID

    members = channel.members #finds members connected to the channel

    inputFile = open("old.txt", "r")
    readFile = inputFile.read()

    oldMemIds = []

    for id in readFile.split():
        oldMemIds.append(id)

    inputFile.close()


    
    outputFile = open("old.txt", "w")

    memids = [] #(list)
    for member in members:
        outputFile.write(str(member.id)+" ")
        memids.append(str(member.id))

    outputFile.close()


    

    joinedIds = []
    leftIds = []

    for id in memids:
        if id not in oldMemIds:
            joinedIds.append(id)
            
    for id in oldMemIds:
        if id not in memids:
            leftIds.append(id)

    print(f"{joinedIds} \ {leftIds}")

    announceChannel = bot.get_channel(819745574307889233)

    if joinedIds != []:
        for id in joinedIds:
            if (id != 345729747537494016) and (345729747537494016 not in memids):
                await announceChannel.send(f"<@345729747537494016>, <@{id}> has joined the call")

    if leftIds != []:
        for id in leftIds:
            if (id != 345729747537494016) and (345729747537494016 not in memids):
                await announceChannel.send(f"<@345729747537494016>, <@{id}> has left the call")



    
@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")


# Load environment variables from a .env file
load_dotenv(os.path.join(os.path.dirname(__file__),"API_Token.env"))

bot.run(os.getenv("API_TOKEN"))
