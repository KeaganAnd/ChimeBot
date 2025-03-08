import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import sys



# Retrieve bot prefix from environment variables
botPrefix = 'c'

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix=[botPrefix.upper(), botPrefix.lower()], intents=discord.Intents.all())
bot.remove_command('help')  # Removes default help command

# Define guild object
guild = discord.Object(id=699814917624037478)

# List to keep track of last checked members
lastCheckMembers = []

#To skip loop, if the channel is changed so it doesn't send 'left' messages
skipLoop = True 

#Settings dictionary
settings = {}
settingsLineNumber = {}

try: #Open config and write settings to dict

    with open('Config.txt', 'r') as file:
        readFile = file.readlines()
        amountOfLines = len(readFile)
    
    for lineNumber,line in enumerate(readFile):
        if line[0] == '#' or line[0] == '\n':
            continue
        splitLine = line.split("=")


        if len(splitLine) != 1:
            splitLine[1] = splitLine[1].strip("\n")
            
            settings[splitLine[0]] = (splitLine[1])
            settingsLineNumber[splitLine[0]] = lineNumber+1
    file.close()
except FileNotFoundError: #If config file doesnt exit then create it and close program
    with open('Config.txt', 'w') as file:
            file.write("#EDIT ME\nBotToken=YOURAPIKEY\n#------------\nMonitoredChannel=\n#This is the voice channel the bot will monitor\n\nSendChannel=\n#This is the text channel the bot will send notifications to\n\nBotPrefix=c\n#The prefix used for commands (dont really need to change this one)")
            file.close()
            print("Welcome new user! Please enter your Discord Bot API Key in \'Config.txt\'")
            sys.exit()

#Functions

def updateConfig(key:str, value): #Updates the local dictionary and saves to config file.
    with open("Config.txt", 'r+') as file:
        readFile = file.readlines()
        print(readFile)

        readFile[settingsLineNumber[key]-1] = f"{key}={value}"
        settings[key] = value
        #NEED TO CLEAR TEXT FILE
        file.writelines(readFile)
        file.close()


MonitoredChannel=1244866756695036006
SendChannel=1346322873077469224

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f"[-----------------------]\n{os.path.basename(__file__)[0:-3]} Ready\n[-----------------------]")
    checkVC.start()  # Start the voice channel check loop

@tasks.loop(seconds=5)
async def checkVC():
    """Loop to check the voice channel for member changes."""
    global skipLoop
    
    global lastCheckMembers
    channel = bot.get_channel(MonitoredChannel)  # Get the monitored channel

    try:
        connectedMembers = channel.members  # Get members connected to the channel
    except AttributeError:
        print("A channel has not been set to monitor")
        return

    connectedMembersID = [member.id for member in connectedMembers]

    joinedMembers = []
    leftMembers = []

    for member in connectedMembersID:
        if member not in lastCheckMembers:
            joinedMembers.append(member)

    for member in lastCheckMembers:
        if member not in connectedMembersID:
            leftMembers.append(member)

    if len(joinedMembers)+len(leftMembers) > 0:
        print(f"{joinedMembers} \\ {leftMembers}")
    else:
        print("No Changes")

    announceChannel = bot.get_channel(SendChannel)  # Get the announcement channel

    if skipLoop:
        skipLoop = False
        lastCheckMembers = connectedMembersID
        return
    
    if joinedMembers:
        for id in joinedMembers:
            await announceChannel.send(f"<@{id}> has joined the call")

    if leftMembers:
        for id in leftMembers:
            await announceChannel.send(f"<@{id}> has left the call")

    lastCheckMembers = connectedMembersID

@bot.command()
async def sync(ctx):
    """Command to sync the bot's command tree."""
    if ctx.author.id == 380178805379301386:
        commandsSynced = await bot.tree.sync(guild=guild)
        await ctx.send(f'{commandsSynced} | Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

@bot.tree.command(name="setmonitorchannel", description="Set the voice channel the bot is watching.", guild=guild)
async def setmonitorchannel(interaction: discord.Interaction, channel: discord.VoiceChannel):
    """Slash command to change the monitored voice channel."""
    await interaction.response.send_message(f"Now monitoring <#{channel.id}>")
    updateConfig("MonitoredChannel",channel.id)
    global skipLoop
    skipLoop = True

@bot.tree.command(name="setsendchannel", description="Set the text channel the bot sends notifications to.", guild=guild)
async def setmonitorchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    """Slash command to change the monitored voice channel."""
    await interaction.response.send_message(f"Now sending notifications to <#{channel.id}>")
    updateConfig("SendChannel",channel.id)
    global skipLoop
    skipLoop = True



# Run the bot
bot.run(settings["BotToken"])


