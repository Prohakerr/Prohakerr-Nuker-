import discord
from pystyle import Write, Colors
import asyncio

async def rename_server(selected_guild):
    bot_member = selected_guild.me

    
    if not bot_member.guild_permissions.manage_guild:
        Write.Print("❌ The bot does not have permission to manage the server.\n", Colors.red, interval=0.0)
        return

    
    new_server_name = input("Enter the new name for the server: ").strip()
    if not new_server_name:
        Write.Print("❌ Please enter a valid server name.\n", Colors.red, interval=0.0)
        return

    try:
        
        await selected_guild.edit(name=new_server_name)
        Write.Print(f"✅ Server renamed successfully to '{new_server_name}'.\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print("❌ Permission denied: Cannot rename the server.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        Write.Print(f"❌ An error occurred while renaming the server: {str(e)}\n", Colors.red, interval=0.0)

    input("Press Enter to continue...")



