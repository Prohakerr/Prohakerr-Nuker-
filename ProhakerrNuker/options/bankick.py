import asyncio
import discord
from pystyle import Write, Colors

async def kick_member(member):
    try:
        await member.kick(reason="Prohakerr.")
        return f"✅ Kicked: {member.name}#{member.discriminator}"
    except discord.Forbidden:
        return f"❌ Permission denied: Cannot kick {member.name}#{member.discriminator}"
    except Exception as e:
        return f"❌ An unexpected error occurred while kicking {member.name}: {str(e)}"

async def ban_member(member):
    try:
        await member.ban(reason="Prohakerr.")
        return f"✅ Banned: {member.name}#{member.discriminator}"
    except discord.Forbidden:
        return f"❌ Permission denied: Cannot ban {member.name}#{member.discriminator}"
    except Exception as e:
        return f"❌ An unexpected error occurred while banning {member.name}: {str(e)}"

async def kick_all_members(selected_guild):
    bot_member = selected_guild.me
    kicked_messages = []

    tasks = []
    for member in selected_guild.members:
        if member != bot_member and member.top_role < bot_member.top_role:
            tasks.append(kick_member(member))

    results = await asyncio.gather(*tasks)
    kicked_messages.extend(results)

    for message in kicked_messages:
        Write.Print(message, Colors.green if "✅" in message else Colors.red, interval=0.0)

async def ban_all_members(selected_guild):
    bot_member = selected_guild.me
    banned_messages = []

    tasks = []
    for member in selected_guild.members:
        if member != bot_member and member.top_role < bot_member.top_role:
            tasks.append(ban_member(member))

    results = await asyncio.gather(*tasks)
    banned_messages.extend(results)

    for message in banned_messages:
        Write.Print(message, Colors.green if "✅" in message else Colors.red, interval=0.0)
