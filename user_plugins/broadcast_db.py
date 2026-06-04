import time
import datetime
import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

from config import Config
from helper.database import db

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("senddb") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast(client, message):

    users = await db.get_all_users()
    total = await db.total_users_count()

    done = 0
    success = 0
    failed = 0

    start = time.time()

    status = await message.reply_text(
        "**Broadcast Started… Please wait ⏳**"
    )

    async for user in users:
        user_id = int(user["id"])
        done += 1

        try:
            await message.reply_to_message.copy(user_id)
            success += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user_id)
            success += 1

        except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
            await db.delete_user(user_id)
            failed += 1

        except Exception as e:
            logger.error(e)
            failed += 1

        if done % 20 == 0:
            await status.edit(
                f"""**Broadcast In Progress**

Total Users : `{total}`
Completed : `{done}`
Success : `{success}`
Failed : `{failed}`
"""
            )

    end = datetime.timedelta(seconds=int(time.time() - start))

    await status.edit(
        f"""**Broadcast Completed ✅**

Time Taken : `{end}`

Total Users : `{total}`
Success : `{success}`
Failed : `{failed}`
"""
    )
