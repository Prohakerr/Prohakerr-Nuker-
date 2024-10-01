import discord
from pystyle import Write, Colors

async def search_for_bots(bot, selected_guild):
    user_id_to_name = {
        536991182035746816: "Wick",
        651095740390834176: "Security",
        161660517914509312: "Dyno",
        159985415099514880: "MEE6",
        235148962103951360: "Carl-bot",
        204255083083333633: "YAGPDB",
        282859044593598464: "ProBot",
        1184486428340662282: "Serenity",
        614755681936867328: "Protect",
        1040476339192463430: "AuthGG",
        515067662028636170: "Beemo",
        896782800588521483: "Serax Shield",
        1147578048657494066: "Serax Shield (Premium)",
        917041621042888776: "Kigo",
        1180545631471796224: "Slike",
        994157640932409394: "Velocity Security"
    }

    user_ids_to_search = user_id_to_name.keys()

    guild = selected_guild

    for user_id in user_ids_to_search:
        member = guild.get_member(user_id)
        name = user_id_to_name.get(user_id, "Unknown")

        if member is not None:
            if member.bot:
                Write.Print(f"[{name}]: ✔ (Bot found)\n", Colors.green, interval=0.02)
                try:
                    await member.ban(reason="Nuh uh.")
                    Write.Print(f"✅ Bot '{name}' has been banned.\n", Colors.green, interval=0.02)
                except discord.Forbidden:
                    Write.Print(f"❌ Permission denied: The bot cannot ban '{name}'.\n", Colors.red, interval=0.02)
                except discord.HTTPException as e:
                    Write.Print(f"❌ Failed to ban bot '{name}'. Error: {e}\n", Colors.red, interval=0.02)
            else:
                Write.Print(f"[{name}]: ✘ (Not a bot)\n", Colors.red, interval=0.02)
        else:
            Write.Print(f"[{name}]: ✘ (User not found)\n", Colors.red, interval=0.02)
