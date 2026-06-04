import os, sys, logging, time, asyncio

from config import Config 
from pyrogram import Client, filters, enums
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid
from helper.utils import get_time

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("chat_broadcast") & (filters.channel | filters.group) & filters.reply)
async def send_to_chat_members(client, message):
    logger.info('hello')
    chat = message.chat
    done = 0
    failed = 0
    success = 0
    skipped = 0
    start_time = time.time()
    content = message.reply_to_message
    
    stt = await client.send_message('me', f"**Broadcast Starred In {chat.title}**")
    sts = await stt.reply("in progress", quote=True)
    
    # Determine how many users to skip
    skip = 0
    if len(message.command) > 1:
        try:
            skip = int(message.command[1])
        except ValueError:
            return await message.reply_text("**Invalid skip value. Please enter a valid number.**", quote=True)
    
    await message.delete()
    # Iterate over chat join requests
    tasks = []
    async for member in client.get_chat_members(chat.id):
        if skip > 0:
            skip -= 1
            skipped += 1
            done += 1
            continue
        
        user_id = member.user.id
        tasks.append(broadcast_messages(client, content, user_id))
        done += 1
        if len(tasks) % 10 == 0:  
            results = await asyncio.gather(*tasks)
            tasks = []
            success += results.count(True)
            failed += results.count(False)
            try: await sts.edit(f"**⟳ ɪɴ ᴩʀᴏɢʀᴇss:\n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}` \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")
            except: pass
            await asyncio.sleep(2)
        
    await sts.edit(f"**✓ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ {get_time(int(time.time() - start_time))}: \n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}` \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")       


async def broadcast_messages(client, message, user_id):
    try:
        await message.copy(chat_id=user_id)
        return True       
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(client, message, user_id)
    except InputUserDeactivated:
        logger.info(f"{user_id} - Account is deactivated.")
        return False
    except UserIsBlocked:
        logger.info(f"{user_id} - Blocked the bot.")
        return False
    except PeerIdInvalid:
        logger.info(f"{user_id} - Invalid PeerId.")
        return False
    except Exception as e:
        logger.error(f"Error broadcasting to {user_id}: {str(e)}", exc_info=True)
        return False
        
        
