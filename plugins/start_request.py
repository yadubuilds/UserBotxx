import time
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from helper.database import db
from config import Config


@Client.on_message(filters.command("start") & filters.private)
async def start_request(client, message):

    if len(message.command) < 2:
        return

    if message.command[1] != "request":
        return

    user = message.from_user
    group_id = Config.GROUPS[0]

    data = await db.add_user(group_id, user, days=7)

    try:
        link = await client.create_chat_invite_link(
            chat_id=group_id,
            member_limit=1,
            expire_date=int(time.time()) + 300
        )

    except ChatAdminRequired:
        return await message.reply(
            "❌ Bot is not admin in the group/channel"
        )

    await message.reply(
        "✅ **Your One-Time Invite Link**\n\n"
        f"🔗 {link.invite_link}\n\n"
        "⚠️ Valid for 5 minutes\n"
        "⚠️ Can be used only once"
    )
