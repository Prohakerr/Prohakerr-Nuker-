from pystyle import Write, Colors
from colorama import Fore
import discord

r = Fore.RED
g = Fore.GREEN

async def check_and_delete_highest_role(bot, selected_guild):
    bot_member = selected_guild.me  
    bot_role = bot_member.top_role  

    highest_role = max(selected_guild.roles, key=lambda role: role.position)

    Write.Print(f"Bot's highest role: {bot_role.name}\n", Colors.green, interval=0.02)

    if highest_role == bot_role:
        Write.Print(f"❌ The bot cannot delete its own highest role.\n", Colors.green_to_cyan, interval=0.02)
        input("Press Enter to continue...")
        return

    try:
        await highest_role.delete(reason="Role deleted by bot command.")
        Write.Print(f"✅ The highest role '{highest_role.name}' has been deleted.\n", Colors.green_to_cyan, interval=0.02)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: The bot cannot delete roles.\n", Colors.green_to_cyan, interval=0.02)
    except discord.HTTPException as e:
        Write.Print(f"❌ Permission denied: The bot cannot delete roles.\n", Colors.green_to_cyan, interval=0.02)