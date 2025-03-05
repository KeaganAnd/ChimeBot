import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Fore, Style
import asyncio
from dotenv import load_dotenv
import os

# Load config file
load_dotenv(os.path.join(os.path.dirname(__file__), "Config.env"))

botPrefix = os.getenv("BotPrefix")

bot = commands.Bot(command_prefix=[botPrefix.upper(), botPrefix.lower()], intents=discord.Intents.all())
bot.remove_command('help')  # Removes default help command

@bot.event
async def on_ready():
    print(Fore.YELLOW + f"[-----------------------]\nRoBot Ready\n[-----------------------]" + Style.RESET_ALL)
    checkVC.start()
    
guild=discord.Object(id=1035736124448047135)

lastCheckMembers = []

@tasks.loop(seconds=5)
async def checkVC():
    global lastCheckMembers
    channel = bot.get_channel(int(os.getenv("MonitoredChannel")))  # Gets the channel you want to get the list from | Needs to take a channel ID

    connectedMembers = channel.members  # Finds members connected to the channel
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
            await announceChannel.send(f"<@{id}> has joined the call")

    if len(leftMembers) > 0:
        for id in leftMembers:
            await announceChannel.send(f"<@{id}> has left the call")

    joinedMembers.clear()
    leftMembers.clear()

    lastCheckMembers = connectedMembersID

@bot.command()
async def sync(ctx):
    if ctx.author.id == 380178805379301386:
        commandsSynced = await bot.tree.sync(guild=guild)
        commandsSynced = await bot.tree.sync()
        await ctx.send(f'{commandsSynced} | Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')


@bot.tree.command(name="changemonitorchannel", description="Set the voice channel the bot is watching.",guild=guild)
async def echo(interaction: discord.Interaction, channel: discord.VoiceChannel):
    await interaction.response.send_message(channel.members)



# Load bot token
load_dotenv(os.path.join(os.path.dirname(__file__), "API_Token.env"))

bot.run(os.getenv("API_TOKEN"))
