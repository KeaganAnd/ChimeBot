import discord
from discord.ext import commands, tasks
import sys

# Retrieve bot prefix from environment variables
botPrefix = 'c'

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix=[botPrefix.upper(), botPrefix.lower()], intents=discord.Intents.all())
bot.remove_command('help')  # Removes default help command

# List to keep track of last checked members
lastCheckMembers = []

#To skip loop, if the channel is changed so it doesn't send 'left' messages
skipLoop = True 

#Settings dictionary
settings = {}
settingsLineNumber = {}


#Functions

def updateConfig(key:str, value): #Updates the local dictionary and saves to config file.
    with open("Config.txt", 'r+') as file:
        readFile = file.readlines()
        try:
            readFile[settingsLineNumber[key]-1] = f"{key}={value}\n"
        except KeyError:
            print("Config file is not configured properly. Please fix your recent changes or delete the file to get a clean file.")
        settings[key] = value
        file.seek(0)
        file.truncate()
        file.writelines(readFile)
        file.close()


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
            
            if splitLine[0] == "AtAGroup": #Handles loading the AtAGroup setting because bools are weird
                if str(splitLine[1]).lower() == "true":
                    settings[splitLine[0]] = True
                elif str(splitLine[1]).lower() == "false":
                        settings[splitLine[0]] = False
                else:
                    print("ERROR: Config.txt incorrectly configured\nAtAGroup is not a valid boolean\nFall back to default of \'False'")
                    settingsLineNumber[splitLine[0]] = lineNumber+1
                    updateConfig("AtAGroup",False)
            else:
                settings[splitLine[0]] = (splitLine[1])
            settingsLineNumber[splitLine[0]] = lineNumber+1
    file.close()
except FileNotFoundError: #If config file doesnt exit then create it and close program
    with open('Config.txt', 'w') as file:
            file.write("#EDIT ME\nBotToken=YOURAPIKEY\n#------------\nMonitoredChannel=\n#This is the voice channel the bot will monitor\n\nSendChannel=\n#This is the text channel the bot will send notifications to\n\nBotPrefix=c\n#The prefix used for commands (dont really need to change this one)\n\n#This determines if a group gets @'d\nAtAGroup=False\n\n#What group gets @'d\nGroupToAt=@everyone\n\n#How often the bot checks the voice channel in seconds (Be careful how low this is set, it can affect performance)\nLoopTime=5\n\n#The server the bot works in\nServerID=") #This is a long string lol
            file.close()
            print("Welcome new user! Please enter your Discord Bot API Key in \'Config.txt\'")
            sys.exit()


# Define guild object
try:
    guild = discord.Object(id=int(settings["ServerID"]))
except ValueError:
    pass


@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f"-----------------------\n      ChimeBot Ready\n-----------------------")
    checkVC.start()  # Start the voice channel check loop

try:
    int(settings["LoopTime"])
except ValueError:
    print("ERROR: Config.txt incorrectly configured\nLoopTime is not a valid whole number\nFall back to default of \'5\'")
    updateConfig("LoopTime",5)

@tasks.loop(seconds=int(settings["LoopTime"]))

async def checkVC():
    """Loop to check the voice channel for member changes."""
    global skipLoop
    global lastCheckMembers

    try:
        guild
    except NameError:
        return

    try:
        MonitoredChannel=int(settings["MonitoredChannel"])
    except ValueError:
        print("A channel has not been set to monitor")
        return

    try:
        SendChannel=int(settings["SendChannel"])
    except ValueError:
        print("A channel has not been set to send messages")
        return

    channel = bot.get_channel(MonitoredChannel)  # Get the monitored channel
    try:
        connectedMembers = channel.members  # Get members connected to the channel
    except AttributeError:
        print("ERROR: Config.txt incorrectly configured\nMonitoredChannel is not a valid channel ID\nFall back to default of \'\'")
        updateConfig("MonitoredChannel","")
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
        print("No Changes...")

    announceChannel = bot.get_channel(SendChannel)  # Get the announcement channel

    if skipLoop:
        skipLoop = False
        lastCheckMembers = connectedMembersID
        return
    
    try:
        if joinedMembers:
            for id in joinedMembers:
                match settings["AtAGroup"]:
                    case False:
                        await announceChannel.send(f"<@{id}> has joined the call")
                    case True:
                        if settings['GroupToAt'] == "@everyone":
                            await announceChannel.send(f"{settings['GroupToAt']}, <@{id}> has joined the call")
                        else:
                            await announceChannel.send(f"<@&{settings['GroupToAt']}>, <@{id}> has joined the call")
        if leftMembers:
            for id in leftMembers:
                match settings["AtAGroup"]:
                    case False:
                        await announceChannel.send(f"<@{id}> has left the call")
                    case True:
                        if settings['GroupToAt'] == "@everyone":
                            await announceChannel.send(f"{settings['GroupToAt']}, <@{id}> has left the call")
                        else:
                            await announceChannel.send(f"<@&{settings['GroupToAt']}>, <@{id}> has left the call")
    except AttributeError:
            print("A channel has not been set to send messages to.")

    lastCheckMembers = connectedMembersID

@bot.command()
async def sync(ctx):
    """Command to sync the bot's command tree."""
    updateConfig("ServerID",ctx.guild.id)
    global guild
    guild = discord.Object(id=int(settings["ServerID"]))
    addCommands()
    await bot.tree.sync(guild=guild)
    await ctx.send('Command tree synced.')

def addCommands():
    @bot.tree.command(name="setmonitorchannel", description="Set the voice channel the bot is watching.", guild=guild)
    async def setmonitorchannel(interaction: discord.Interaction, channel: discord.VoiceChannel):
        """Slash command to change the monitored voice channel."""
        await interaction.response.send_message(f"Now monitoring <#{channel.id}>")
        updateConfig("MonitoredChannel",channel.id)
        global skipLoop
        skipLoop = True

    @bot.tree.command(name="setsendchannel", description="Set the text channel the bot sends notifications to.", guild=guild)
    async def setmonitorchannel(interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash command to change the notif text channel."""
        await interaction.response.send_message(f"Now sending notifications to <#{channel.id}>")
        updateConfig("SendChannel",channel.id)
        global skipLoop
        skipLoop = True

    @bot.tree.command(name="setalertedrole", description="Set the role that is alerted when someone leaves or joins.", guild=guild)
    async def setmonitorchannel(interaction: discord.Interaction, role: discord.Role):
        """Slash command to choose role to @."""
        if str(role) == "@everyone":
            await interaction.response.send_message(f"Now sending notifications to {role}")
            updateConfig("GroupToAt", str(role))
        else:
            await interaction.response.send_message(f"Now sending notifications to <@&{role.id}>")
            updateConfig("GroupToAt",role.id)

    @bot.tree.command(name="atagroup", description="Set whether or not a group will be @'d", guild=guild)
    async def setmonitorchannel(interaction: discord.Interaction, bool: bool):
        """Slash command to choose if role should be @'d."""
        await interaction.response.send_message(f"Sending notifications: **{bool}**")
        updateConfig("AtAGroup", bool)

try:
    addCommands()
except NameError:
    print("ERROR: Server not setup please use \'csync\'")




# Run the bot
try:
    bot.run(settings["BotToken"])
except discord.errors.LoginFailure:
    if settings["BotToken"] == "YOURAPIKEY":
        print("Welcome new user! Please enter your Discord Bot API Key in \'Config.txt\'")
    else:
        print(f"Your bot token is not valid: {settings["BotToken"]}")
except discord.errors.PrivilegedIntentsRequired:
    print("Please read step two in the setup under README.md to learn more about how to enable privileged intent.")
    sys.exit()