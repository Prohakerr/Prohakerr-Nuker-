import discord  
from pystyle import Write, Colors  
import asyncio


async def create_single_channel(selected_guild, channel_name, channel_type):
    try:
        if channel_type == "text":
            await selected_guild.create_text_channel(channel_name)
        elif channel_type == "voice":
            await selected_guild.create_voice_channel(channel_name)
        Write.Print(f"✅ Channel '{channel_name}' created successfully as a {channel_type} channel.\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: Cannot create channel '{channel_name}'.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        if e.code == 50013:
            Write.Print("❌ Permission denied: The bot cannot create channels.\n", Colors.red, interval=0.0)
        else:
            Write.Print(f"❌ Failed to create channel '{channel_name}' due to an error: {str(e)}\n", Colors.red, interval=0.0)
    except discord.RateLimited as rate_limit_error:
        Write.Print(f"❌ Rate limit hit! Waiting {rate_limit_error.retry_after} seconds before retrying '{channel_name}'...\n", Colors.red, interval=0.0)
        await asyncio.sleep(rate_limit_error.retry_after)
        await create_single_channel(selected_guild, channel_name, channel_type)  

async def create_channel(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_channels:
        Write.Print("❌ The bot does not have permission to manage channels.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    
    channel_type = input("Enter the type of channel to create (text/voice): ").strip().lower()

    if channel_type not in ["text", "voice"]:
        Write.Print("❌ Invalid channel type. Please enter 'text' or 'voice'.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    
    base_name = input("Enter the base name for the channels: ").strip()
    if not base_name:
        Write.Print("❌ Please enter a valid base name.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    try:
        amount = int(input("Enter the number of channels to create: "))
        if amount <= 0:
            Write.Print("❌ Please enter a positive number.\n", Colors.red, interval=0.0)
            input("Press Enter to continue...")
            return
    except ValueError:
        Write.Print("❌ Invalid number. Please enter a valid integer.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    Write.Print(f"Creating {amount} {channel_type} channels...\n", Colors.green, interval=0.0)

    tasks = []
    for i in range(amount):
        channel_name = f"{base_name}-{i + 1}"
        tasks.append(create_single_channel(selected_guild, channel_name, channel_type))

    await asyncio.gather(*tasks)

    Write.Print(f"✅ Finished creating {amount} channels!\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
