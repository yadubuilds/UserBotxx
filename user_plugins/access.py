from pyrogram import Client, filters
from config import Config


@Client.on_message(filters.command("access") & filters.private)
async def send_access_link(client, message):

    if message.from_user.id not in Config.ADMINS:
        return

    bot_link = f"https://t.me/{Config.BOT_UN}?start=request"

    await message.reply(
        "✅ Access granted\n\n"
        "👉 Click below to get your invite link:\n\n"
        f"{bot_link}"
    )
