import time, asyncio, datetime, asyncio, logging

from config import Config 
from pyrogram import Client, filters, enums, raw
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from helper.utils import get_time

logger = logging.getLogger(__name__)

@Client.on_message(filters.command('sendall') & filters.reply & filters.private & filters.user('self'))
async def broadcast_all(client, message):
    broadcast_msg = message.reply_to_message
    done = 0
    failed = 0
    success = 0
    skipped = 0
    skip = 0
    if len(message.command) > 1:
        try:
            skip = int(message.command[1])
        except ValueError:
            return await message.reply_text("**Invalid skip value. Please enter a valid number.**", quote=True)
    
    sts = await message.reply_text("**Broadcasting to all users...**", quote=True)
    start_time = time.time()
    
    tasks = []
    async for dialog in client.get_dialogs():
        if skip > 0:
            skip -= 1
            skipped += 1
            done += 1
            continue
        
        if dialog.chat.type != enums.ChatType.PRIVATE: continue
        try: user = await client.get_users(dialog.chat.id)
        except: continue
        tasks.append(broadcast_messages(client, message.reply_to_message, dialog.chat.id))
        done += 1
        if len(tasks) % 10 == 0:  
            results = await asyncio.gather(*tasks)
            tasks = []
            success += results.count(True)
            failed += results.count(False)
            try: await sts.edit(f"**Broadcasting to all users:\n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}` \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")
            except: pass
        await asyncio.sleep(1)
        
    if len(tasks) > 0:  
        results = await asyncio.gather(*tasks)
        tasks = []    
        success += results.count(True)
        failed += results.count(False)
    await sts.edit(f"**✓ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ {get_time(int(time.time() - start_time))}: \n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}`  \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")    
    

@Client.on_message(filters.command('sendcon') & filters.reply & filters.private & filters.user('self'))
async def broadcast_contact(client, message):
    broadcast_msg = message.reply_to_message
    done = 0
    failed = 0
    success = 0
    skipped = 0
    skip = 0
    if len(message.command) > 1:
        try:
            skip = int(message.command[1])
        except ValueError:
            return await message.reply_text("**Invalid skip value. Please enter a valid number.**", quote=True)
    
    sts = await message.reply_text("**Broadcasting to contacts...**", quote=True)
    start_time = time.time()
    
    tasks = []
    async for dialog in client.get_dialogs():
        if skip > 0:
            skip -= 1
            skipped += 1
            done += 1
            continue
        
        if dialog.chat.type != enums.ChatType.PRIVATE: continue
        try: user = await client.get_users(dialog.chat.id)
        except: continue
        if user.is_contact: 
            tasks.append(broadcast_messages(client, message.reply_to_message, dialog.chat.id))
            done += 1
            if len(tasks) % 10 == 0:  
                results = await asyncio.gather(*tasks)
                tasks = []
                success += results.count(True)
                failed += results.count(False)
                try: await sts.edit(f"**Broadcasting to contacts:\n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}` \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")
                except: pass
            await asyncio.sleep(1)
        
    if len(tasks) > 0:  
        results = await asyncio.gather(*tasks)
        tasks = []    
        success += results.count(True)
        failed += results.count(False)
    await sts.edit(f"**✓ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ɪɴ {get_time(int(time.time() - start_time))}: \n\nᴄᴏᴍᴩʟᴇᴛᴇᴅ: `{done}` \nꜱᴜᴄᴄᴇꜱꜱ: `{success}` \nꜰᴀɪʟᴇᴅ: `{failed}`  \nꜱᴋɪᴩᴩᴇᴅ: `{skipped}`**")    
    

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
        

