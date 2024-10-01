import discord
from pystyle import Write, Colors
import asyncio

async def rename_channel(channel, new_channel_name):
    try:
        await channel.edit(name=new_channel_name)
        Write.Print(f"✅ Renamed channel '{channel.name}' to '{new_channel_name}'.\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: Cannot rename channel {channel.name}.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        Write.Print(f"❌ An error occurred while renaming channel {channel.name}: {str(e)}\n", Colors.red, interval=0.0)
    except discord.RateLimited as rate_limit_error:
        Write.Print(f"❌ Rate limit hit! Waiting {rate_limit_error.retry_after} seconds before retrying...\n", Colors.red, interval=0.0)
        await asyncio.sleep(rate_limit_error.retry_after)
        await rename_channel(channel, new_channel_name)

async def rename_all_channels(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_channels:
        Write.Print("❌ The bot does not have permission to manage channels.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    new_base_name = input("Enter the new base name for the channels: ").strip()
    if not new_base_name:
        Write.Print("❌ Please enter a valid base name.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    channels = selected_guild.channels

    if not channels:
        Write.Print("❌ No channels available in this guild.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    Write.Print(f"Renaming {len(channels)} channels...\n", Colors.green, interval=0.0)

    tasks = []
    for i, channel in enumerate(channels):
        new_channel_name = f"{new_base_name}-{i + 1}"
        tasks.append(rename_channel(channel, new_channel_name))

    await asyncio.gather(*tasks)

    Write.Print("✅ All channels renamed!\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
