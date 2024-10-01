import discord
from pystyle import Write, Colors
import asyncio

async def create_role(role_name, selected_guild):
    try:
        role = await selected_guild.create_role(name=role_name)
        Write.Print(f"✅ Role '{role_name}' created successfully.\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print("❌ Permission denied: The bot cannot create roles.\n", Colors.red, interval=0.0)
        return False  
    except discord.HTTPException as e:
        if e.status == 429:  
            retry_after = e.retry_after  
            Write.Print(f"❌ Rate limit hit! Waiting {retry_after:.2f} seconds before retrying...\n", Colors.red, interval=0.0)
            return retry_after  
        Write.Print(f"❌ Failed to create role '{role_name}' due to an error: {str(e)}\n", Colors.red, interval=0.0)
        return False  
    return True  

async def create_roles(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_roles:
        Write.Print("❌ The bot does not have permission to manage roles.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    
    base_name = input("Enter the base name for the roles: ").strip()
    if not base_name:
        Write.Print("❌ Please enter a valid base name.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    
    try:
        amount = int(input("Enter the number of roles to create: "))
        if amount <= 0:
            Write.Print("❌ Please enter a positive number.\n", Colors.red, interval=0.0)
            input("Press Enter to continue...")
            return
    except ValueError:
        Write.Print("❌ Invalid number. Please enter a valid integer.\n", Colors.red, interval=0.0)
        input("Press Enter to continue...")
        return

    Write.Print(f"Attempting to create {amount} roles...\n", Colors.green, interval=0.0)

    index = 0
    rate_limit_wait = 0

    while index < amount:
        current_tasks = []
        for i in range(5):  
            if index < amount:
                role_name = f"{base_name}-{index + 1}"
                current_tasks.append(create_role(role_name, selected_guild))
                index += 1

        results = await asyncio.gather(*current_tasks)

        
        for result in results:
            if result is not True:  
                if result:  
                    rate_limit_wait = max(rate_limit_wait, result)

        if rate_limit_wait:
            Write.Print(f"❌ Waiting {rate_limit_wait:.2f} seconds due to rate limit...\n", Colors.red, interval=0.0)
            await asyncio.sleep(rate_limit_wait)
            rate_limit_wait = 0  

    Write.Print("✅ Finished creating all roles.\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
