import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Fore, Style
import asyncio
from dotenv import load_dotenv, set_key
import os

# Load config file
load_dotenv(os.path.join(os.path.dirname(__file__), "Config.env"))

# Retrieve bot prefix from environment variables
botPrefix = os.getenv("BotPrefix")

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix=[botPrefix.upper(), botPrefix.lower()], intents=discord.Intents.all())
bot.remove_command('help')  # Removes default help command

# Define guild object
guild = discord.Object(id=699814917624037478)

# List to keep track of last checked members
lastCheckMembers = []

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(Fore.YELLOW + f"[-----------------------]\nRoBot Ready\n[-----------------------]" + Style.RESET_ALL)
    checkVC.start()  # Start the voice channel check loop
    await bot.tree.sync()  # Sync the slash commands

@tasks.loop(seconds=5)
async def checkVC():
    """Loop to check the voice channel for member changes."""
    global lastCheckMembers
    channel = bot.get_channel(int(os.getenv("MonitoredChannel")))  # Get the monitored channel

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

    print(f"{joinedMembers} \\ {leftMembers}")

    announceChannel = bot.get_channel(int(os.getenv("SendChannel")))  # Get the announcement channel

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

@bot.tree.command(name="changemonitorchannel", description="Set the voice channel the bot is watching.", guild=guild)
async def changemonitorchannel(interaction: discord.Interaction, channel: discord.VoiceChannel):
    """Slash command to change the monitored voice channel."""
    await interaction.response.send_message(f"Now monitoring <#{channel.id}>")
    os.environ["MonitoredChannel"] = str(channel.id)
    set_key(dotenv_path=(os.path.join(os.path.dirname(__file__), "Config.env")), key_to_set="MonitoredChannel", value_to_set=str(channel.id))

# Load bot token
load_dotenv(os.path.join(os.path.dirname(__file__), "API_Token.env"))

# Run the bot
bot.run(os.getenv("API_TOKEN"))


