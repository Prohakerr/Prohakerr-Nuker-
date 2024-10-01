import discord
from pystyle import Write, Colors
import random
import string
import asyncio
import threading

spam_active = False

async def send_message(channel, message_to_send):
    try:
        await channel.send(message_to_send)
        Write.Print(f"✅ Sent message in {channel.name}.\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Forbidden: Cannot send message in channel {channel.name}.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        Write.Print(f"❌ HTTP Exception while sending message: {str(e)}.\n", Colors.red, interval=0.0)

async def start_spamming(selected_guild, spam_message, use_random_string, should_ping_users):
    global spam_active
    Write.Print("✅ Starting spamming! Press 'Enter' to stop\n", Colors.green, interval=0.0)

    while spam_active:
        tasks = []
        for channel in selected_guild.text_channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(selected_guild.me).send_messages:
                message_to_send = f"{spam_message} {' '.join(random.choices(string.ascii_letters + string.digits, k=10))}" if use_random_string else spam_message

                if should_ping_users and selected_guild.members:
                    random_member = random.choice(selected_guild.members)
                    message_to_send = f"{random_member.mention} {message_to_send}"

                tasks.append(asyncio.create_task(send_message(channel, message_to_send)))

        if tasks:
            await asyncio.gather(*tasks)
        
        await asyncio.sleep(0.1)

async def spam_channels(selected_guild):
    global spam_active
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.send_messages:
        Write.Print("❌ The bot does not have permission to send messages in channels.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    spam_message = input("Enter the message to spam: ")
    if not spam_message:
        Write.Print("❌ Please enter a valid message.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    use_random_string = input("Use a random string after the message? (y/n): ").strip().lower() == 'y'
    should_ping_users = input("Ping random users? (y/n): ").strip().lower() == 'y'
    spam_active = True

    threading.Thread(target=wait_for_stop).start()
    await start_spamming(selected_guild, spam_message, use_random_string, should_ping_users)

def wait_for_stop():
    global spam_active
    while spam_active:
        if input() == '':
            spam_active = False
            Write.Print("Spam has been stopped.\n", Colors.red, interval=0.0)
            break