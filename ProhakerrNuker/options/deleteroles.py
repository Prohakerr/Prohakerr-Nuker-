import discord
from pystyle import Write, Colors
import asyncio

async def delete_role(role):
    try:
        await role.delete()
        Write.Print(f"✅ Deleted role: {role.name}\n", Colors.green, interval=0.0)
    except discord.Forbidden:
        Write.Print(f"❌ Permission denied: Cannot delete role {role.name}.\n", Colors.red, interval=0.0)
    except discord.HTTPException as e:
        if e.status == 429:  
            retry_after = e.retry_after  
            return retry_after  
        else:
            Write.Print(f"❌ An error occurred while deleting role {role.name}: {str(e)}\n", Colors.red, interval=0.0)

async def delete_all_roles(selected_guild):
    bot_member = selected_guild.me

    if not bot_member.guild_permissions.manage_roles:
        Write.Print("❌ The bot does not have permission to manage roles.\n", Colors.red, interval=0.0)
        return

    roles = selected_guild.roles
    roles_to_delete = [role for role in roles if role != selected_guild.default_role and role != bot_member.top_role]

    if len(roles_to_delete) == 0:
        Write.Print("❌ No roles available to delete.\n", Colors.red, interval=0.0)
        return

    Write.Print(f"Attempting to delete {len(roles_to_delete)} roles...\n", Colors.green, interval=0.0)

    total_roles = len(roles_to_delete)
    index = 0
    while index < total_roles:
        current_tasks = []
        rate_limit_wait = 0
        
        for _ in range(10):  
            if index < total_roles:
                current_tasks.append(delete_role(roles_to_delete[index]))
                index += 1
        
        results = await asyncio.gather(*current_tasks)

        for result in results:
            if result:  
                rate_limit_wait = max(rate_limit_wait, result)

        if rate_limit_wait:
            Write.Print(f"❌ Waiting {rate_limit_wait:.2f} seconds due to rate limit...\n", Colors.red, interval=0.0)
            await asyncio.sleep(rate_limit_wait)

    Write.Print("✅ Finished deleting all roles.\n", Colors.green, interval=0.0)
    input("Press Enter to continue...")
