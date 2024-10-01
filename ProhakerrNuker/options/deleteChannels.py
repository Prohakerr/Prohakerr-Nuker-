import discord
from pystyle import Write, Colors
import asyncio

async def delete_single_channel(channel):
    try:
        await channel.delete()
        Write.Print(f"✅ Deleted channel: {channel.name}\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: Cannot delete channel {channel.name}.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        Write.Print(f"❌ An error occurred while deleting channel {channel.name}: {str(e)}\n", Colors.red, interval=0.0)
    except discord.RateLimited as rate_limit_error:
        Write.Print(f"❌ Rate limit hit! Waiting {rate_limit_error.retry_after} seconds before trying to delete '{channel.name}'...\n", Colors.red, interval=0.0)
        await asyncio.sleep(rate_limit_error.retry_after)
        await delete_single_channel(channel)  

async def delete_all_channels(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_channels:
        Write.Print("❌ The bot does not have permission to manage channels.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    channels = selected_guild.channels  

    if not channels:
        Write.Print("❌ No channels available in this guild.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    Write.Print(f"Deleting {len(channels)} channels...\n", Colors.green, interval=0.0)

    tasks = [delete_single_channel(channel) for channel in channels]
    await asyncio.gather(*tasks)
    Write.Print("✅ Finished deleting all channels!\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
