import discord
from pystyle import Write, Colors
import asyncio
import re

async def mute_member(member, duration):
    try:
        await member.timeout(duration, reason="Noob.")
        Write.Print(f"✅ Muted member: {member.display_name}\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: Cannot mute member {member.display_name}.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        Write.Print(f"❌ An error occurred while muting member {member.display_name}: {str(e)}\n", Colors.red, interval=0.0)

async def mute_all_members(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_roles:
        Write.Print("❌ The bot does not have permission to manage roles.\n", Colors.red, interval=0.0)
        return

    duration_input = input("Enter the duration to mute all members (e.g., 10m, 1h, 7d): ").strip()

    duration_regex = re.compile(r'(\d+)([smhd])')
    matches = duration_regex.findall(duration_input)

    total_seconds = 0

    for amount, unit in matches:
        amount = int(amount)
        if unit == 's':
            total_seconds += amount
        elif unit == 'm':
            total_seconds += amount * 60
        elif unit == 'h':
            total_seconds += amount * 3600
        elif unit == 'd':
            total_seconds += amount * 86400

    if total_seconds <= 0:
        Write.Print("❌ Invalid duration provided. Please enter a valid duration.\n", Colors.red, interval=0.0)
        return

    Write.Print(f"Muting all members for {total_seconds} seconds...\n", Colors.green, interval=0.0)

    tasks = []
    for member in selected_guild.members:
        if not member.bot:
            tasks.append(mute_member(member, discord.utils.utcnow() + discord.timedelta(seconds=total_seconds)))

    await asyncio.gather(*tasks)

    Write.Print("✅ Finished muting all members.\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
