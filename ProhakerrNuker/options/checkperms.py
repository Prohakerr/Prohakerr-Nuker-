from pystyle import Write, Colors
from colorama import Fore

r = Fore.RED
g = Fore.GREEN


async def check_bot_permissions(bot, selected_guild):
    bot_member = selected_guild.me  
    permissions = bot_member.guild_permissions  

    Write.Print("Bot Permissions:\n", Colors.green, interval=0.02)
    
    for permission, value in permissions:
        status = "✔" if value else "✘"  
        Write.Print(f"{permission}: {status}\n", Colors.green_to_cyan, interval=0.02)



