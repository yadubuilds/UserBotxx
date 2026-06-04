import os, time, datetime, asyncio, logging
from config import Config
from helper.database import db
from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.private & filters.reply)
async def send_broadcast(client, message):
    all_users = await db.get_all_users()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0

    if len(message.command) != 1:
        skip = message.text.split(' ', 1)[1]
        all_users.skip(int(skip))
        done += int(skip)
    sts = await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ꜱᴛᴀʀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴡʜɪʟᴇ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ✨**", quote=True)
    start_time = time.time()
    tasks = []
    async for user in all_users:
        tasks.append(broadcast_messages(user_id=int(user['id']), message=message.reply_to_message))
        done += 1
        if len(tasks) % 20 == 0: 
            results = await asyncio.gather(*tasks)
            tasks = []
            success += results.count(True)
            failed += results.count(False)
            try: await sts.edit(f"**⟳ ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴩʀᴏɢʀᴇss:\n\nᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ `{total_users}`\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}`**")    
            except: pass
            await asyncio.sleep(2)
    if tasks: 
        results = await asyncio.gather(*tasks)
        success += results.count(True)
        failed += results.count(False)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.delete()
    await message.reply_text(f"**✓ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ {completed_in}: \n\nᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ `{total_users}`\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}`**", quote=True)    
    

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value + 2)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(user_id)
        logger.info(f"{user_id} - Removed from database, since account is deactivated.")
        return False
    except UserIsBlocked:
        #await db.delete_user(user_id)
        logger.info(f"{user_id} - Blocked the bot.")
        return False
    except PeerIdInvalid:
        await db.delete_user(user_id)
        logger.info(f"{user_id} - Invalid PeerId.")
        return False
    except Exception as e:
        logger.error(f"Error broadcasting to {user_id}: {str(e)}", exc_info=True)
        return False


       

        
