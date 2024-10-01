import discord
from pystyle import Write, Colors
import asyncio
import threading

spam_active = False

async def send_dm(member, message):
    try:
        await member.send(message)
        Write.Print(f"✅ Sent message to {member.display_name}: {message}\n", Colors.green, interval=0.000)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied to send DM to {member.display_name}.\n", Colors.red, interval=0.000)
    except discord.HTTPException as e:
        Write.Print(f"❌ Failed to send DM to {member.display_name}: {str(e)}\n", Colors.red, interval=0.000)
    except Exception as e:
        Write.Print(f"❌ An unexpected error occurred: {str(e)}\n", Colors.red, interval=0.000)

async def spam_dm(member, message):
    global spam_active
    while spam_active:
        await send_dm(member, message)

async def dm_all_members(selected_guild):
    global spam_active
    
    message = input("Enter the message you want to send: ").strip()
    if not message:
        Write.Print("❌ Please enter a valid message.\n", Colors.red, interval=0.000)
        return

    spam = input("Do you want to send this message indefinitely? (y/n): ").strip().lower()
    if spam not in ['y', 'n']:
        Write.Print("❌ Please enter 'y' for yes or 'n' for no.\n", Colors.red, interval=0.000)
        return

    is_spam = spam == 'y'

    tasks = []

    for member in selected_guild.members:
        if not member.bot:
            if is_spam:
                tasks.append(spam_dm(member, message))
            else:
                tasks.append(send_dm(member, message))

    if is_spam:
        spam_active = True
        Write.Print("✅ Starting spamming... Press 'Enter' to stop.\n", Colors.green, interval=0.000)
        threading.Thread(target=wait_for_stop).start()
        await asyncio.gather(*tasks)
    else:
        await asyncio.gather(*tasks)

def wait_for_stop():
    while True:
        if input() == '':
            global spam_active
            spam_active = False
            Write.Print("Spam has been stopped.\n", Colors.red, interval=0.000)
            break
        asyncio.sleep(0.1)
