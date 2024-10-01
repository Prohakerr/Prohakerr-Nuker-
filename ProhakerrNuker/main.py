import os
import subprocess
import sys

def install(package):
    subprocess.run([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

required_packages = [
    "pystyle",
    "fade",
    "discord.py",
    "colorama"
]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        try:
            install(package)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
            sys.exit(1)

import discord
from discord.ext import commands
import asyncio
import fade
from pystyle import Write, Colors, Center
from options.checkhighestrole import check_and_delete_highest_role
from options.checkperms import check_bot_permissions
from options.antinukebots import search_for_bots
from options.createChannels import create_channel
from options.createRoles import create_roles
from options.spamchannels import spam_channels
from options.deleteChannels import delete_all_channels
from options.renameChannels import rename_all_channels
from options.deleteroles import delete_all_roles
from options.changeservername import rename_server
from options.massDm import dm_all_members
from options.bankick import kick_all_members
from options.bankick import ban_all_members
from options.ultimate import ultimate

    
def get_bot_token():
    try:
        with open('token.txt', 'r') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print("Error: token.txt file not found.")
        sys.exit(1)

async def login_bot():
    token = get_bot_token()
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Logged in as: {bot.user.name}#{bot.user.discriminator}\n')
        await bot.change_presence(activity=discord.Game("Powered By Prohakerr"))
        selected_guild = await list_guilds(bot)
        os.system('cls' if os.name == 'nt' else 'clear')
        await start_gui(bot, selected_guild)

    try:
        await bot.start(token)
    except Exception as e:
        print(f"Error starting bot: {e}")
        await asyncio.sleep(5)
        sys.exit(1)

async def list_guilds(bot):
    print("\nThe bot is in the following guilds:\n")
    for i, guild in enumerate(bot.guilds, start=1):
        Write.Print(f"{i}. {guild.name}\n", Colors.green_to_cyan, interval=0.01)

    selected_guild = None
    while selected_guild is None:
        try:
            choice = int(input("\nSelect a guild by entering its number: "))
            if 1 <= choice <= len(bot.guilds):
                selected_guild = bot.guilds[choice - 1]
                Write.Print(f"\nSelected guild: {selected_guild.name}\n", Colors.green, interval=0.02)
            else:
                print("Invalid number, please try again.")
        except ValueError:
            print("Please enter a valid number.")
    return selected_guild

def logo(username, discriminator, server):
    Logo = f"""
                        Logged in as: {username}#{discriminator}
██████╗ ██████╗  ██████╗ ██╗  ██╗ █████╗ ██╗  ██╗███████╗██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗██║  ██║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗
██████╔╝██████╔╝██║   ██║███████║███████║█████╔╝ █████╗  ██████╔╝██████╔╝
██╔═══╝ ██╔══██╗██║   ██║██╔══██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██╗
██║     ██║  ██║╚██████╔╝██║  ██║██║  ██║██║  ██╗███████╗██║  ██║██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                                         

                              Server: {server}
    """
    centered_ascii = Center.XCenter(Logo)
    faded = fade.brazil(centered_ascii)
    print(faded)

def choices():
    Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ Checks:                            ⦘ | ⦗ Main: \n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [1] Check for known antinuke bots  ⦘ | ⦗ [4] Create channels   ⦘ | ⦗ [12] Spam DM\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [2] Highest role                   ⦘ | ⦗ [5] Delete channels   ⦘ | ⦗ [13] Rename server\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [3] Check Bot Permissions.         ⦘ | ⦗ [6] Rename Channels   ⦘ | ⦗ [14] ULTIMATE DESTRUCTION!\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [N/A]                              ⦘ | ⦗ [7] Kick all          ⦘ | ⦗\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [N/A]                              ⦘ | ⦗ [8] Ban all           ⦘ | ⦗\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [N/A]                              ⦘ | ⦗ [9] Spam channels     ⦘ | ⦗\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [N/A]                              ⦘ | ⦗ [10] Create roles     ⦘ | ⦗\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("⦗ [N/A]                              ⦘ | ⦗ [11] Delete roles     ⦘ | ⦗\n", Colors.green_to_cyan, interval=0.000)
    Write.Print("", Colors.green_to_cyan, interval=0.000)
    Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", Colors.green_to_cyan, interval=0.000)

async def start_gui(bot, selected_guild):
    logo(bot.user.name, bot.user.discriminator, selected_guild.name)
    
    while True:
        choices()
        Write.Print('└──╼ $ Choice: ', Colors.green_to_cyan, interval=0.03)
        choice = input()    
        
        if choice.lower() == "exit":
            sys.exit()
        elif choice == '1':
            await search_for_bots(bot, selected_guild)
            input("Press Enter to continue...")
        elif choice == '2':
            await check_and_delete_highest_role(bot, selected_guild)
            input("Press Enter to continue...")
        elif choice == '3':
            await check_bot_permissions(bot, selected_guild)
            input("Press Enter to continue...")
        elif choice == '4':
            await create_channel(selected_guild)
        elif choice == '5':
            await delete_all_channels(selected_guild)
        elif choice == '6':
            await rename_all_channels(selected_guild)
        elif choice == '7':
            await kick_all_members(selected_guild)
            input("Press Enter to continue...")
        elif choice == '8':
            await ban_all_members(selected_guild)
            input("Press Enter to continue...")
        elif choice == '9':
            await spam_channels(selected_guild)
            input("Press Enter to continue...")
        elif choice == '10':

            await create_roles(selected_guild)
        elif choice == '11':
            await delete_all_roles(selected_guild)
        elif choice == '12':
            await dm_all_members(selected_guild)
            input("Press Enter to continue...")
        elif choice == '13':
            await rename_server(selected_guild)
        elif choice == '14':
            await ultimate(selected_guild)
            input("Press Enter to continue...")
        else:
            Write.Print(f"Please select a valid choice.", Colors.green, interval=0.02)

        os.system('cls' if os.name == 'nt' else 'clear')
        logo(bot.user.name, bot.user.discriminator, selected_guild.name)

if __name__ == "__main__":
    asyncio.run(login_bot())
