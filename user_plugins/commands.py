import asyncio, os, sys, datetime, pytz, time, re, logging

from helper.utils import get_date_for_contact
from pyrogram import Client, filters, enums
from datetime import timedelta, datetime
from helper.database import db
from config import Config, Txt
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
 

@Client.on_message(filters.command('g') & filters.private & filters.user('self'))                       
async def gen_link(client, message):
    try:
        cmd, id, days = message.text.split(' ')
        days = int(days)
        group_id = Config.GROUPS[int(id)]
    except Exception as e:
        return await message.edit(e)
    
    try: chat = await client.get_chat(group_id)
    except: return await message.edit("ultra")

    user = await client.get_users(message.chat.id)
    
    # add to contact 
    try:
        exp = get_date_for_contact(days)
        title = f"{exp} | {user.fullname}"
        await client.add_contact(user.id, title)
    except Exception as e:
        print(e)
        
    add = await db.add_user(group_id, user, days)
    # if add:
    link = f"https://t.me/{Config.BOT_UN}?start=Member_{add['_id']}"
    return await message.edit(f"Successfull ✅\n\n Your Link: {link}")

    # await message.edit("You'Re Already Added") 


@Client.on_message(filters.command('r') & filters.private & filters.user('self'))                       
async def remove(client, message):
    user_id = message.chat.id
    user = await db.get_user(user_id)
    if user:
        group_id = int(user['group_id'])
        await db.delete_user(user_id)
        
        try:
            await client.delete_contacts(user_id)
        except Exception as e:
            print(e) 

        try: chat = await client.get_chat(group_id)
        except: return await message.edit("group id invalid or i am not admin")
        try:
            await client.ban_chat_member(chat.id, user_id)
            await client.unban_chat_member(chat.id, user_id)
        except Exception as e:
            return await message.edit(f"Filed To Remove user from {chat.title}")

        return await message.edit("You can join now.") 

    await message.delete()

@Client.on_message(filters.command("link") & filters.private & filters.user('self'))
async def send_link(c, m):
    try:
        id = int(m.text.split(' ', 1)[1])
        chat_id = Config.GROUPS[id]
    except Exception as e:
        return await m.edit(e)
    try:
        user = await c.get_users(m.chat.id)
        chat = await c.get_chat(chat_id)
        link = await c.create_chat_invite_link(int(chat_id), member_limit=1)
    except Exception as e:
        return await m.edit(e)
    
    try:
        text = f"""
Name: {user.full_name}
Un: {user.username}
Id: `{user.id}`
mention: {user.mention}
Link: **[CLICK HERE](tg://openmessage?user_id={user.id})**

Group: {chat.title}
Link: {chat.invite_link}"""
        await c.send_message(Config.PAYMENT_LOG, text, disable_web_page_preview=True)
    except Exception as e: 
        print(e)   
        
    await m.edit(f"Kidungamani ULTRA welcomes you\n\n**{chat.title}**\n\n\n{link.invite_link}")
 

CUSTOM_NAME = "Mallu🔞"  # Change this to any name you want

@Client.on_message(filters.command("add") & filters.private & filters.user("self"))
async def add_to_contact(c, m):
    try:
        title = CUSTOM_NAME
        await c.add_contact(int(m.chat.id), title)
        await m.delete(True)
    except Exception as e:
        await m.edit(str(e))


@Client.on_message(filters.command("sd") & filters.private & filters.user('self'))          
async def scheduled_message(c, m):
    chat_id = m.chat.id
    await m.delete()
    text = "BRO നമ്മുടെ MAIN ഗ്രൂപ്പ് JULY 1st ഇറങ്ങും, 50,000+ VIDEOS ആയിരിക്കും ഇതിൽ... STAY tuned 😘!!! കൂടാതെ നിങ്ങൾ ഇപ്പോ ഉള്ള ഗ്രൂപ്പ് ഇൽ updation തീർച്ചയും വന്നിരിക്കും!"
    schedule_time = datetime.now() + timedelta(minutes=1)

    await c.send_message(chat_id=chat_id, text=text, schedule_date=schedule_time)


@Client.on_message(filters.command("photo") & filters.private & filters.user('self'))          
async def onec_photo(c, m):
    try:
        await m.delete()
        for photo in Config.PHOTOS:
            try: await m.reply_photo(photo=photo, view_once=True)
            except: continue
    except Exception as e:
        await m.edit(e)

IN_MSG = r"""Kerala Group 😍"""

# Quick Reppy
@Client.on_message(filters.regex(IN_MSG) & filters.private & filters.incoming)
async def send_a1_quick(client, message):
    #A1 = [1, 2, 3, 4, 5, 6, 
    A1 = [21, 22, 23, 24, 25, 26, 27, 28]
    try:
        grouped_ids = set()
        for ms_id in A1:
            schedule_time = datetime.now() + timedelta(seconds=15)
            msg = await client.get_messages(Config.QUICK_REPLY, ms_id)

            if msg.media_group_id:
                await client.copy_media_group(
                    chat_id=message.chat.id, 
                    from_chat_id=Config.QUICK_REPLY, 
                    message_id=msg.id, 
                    schedule_date=schedule_time,
                )  
                continue
            await client.copy_message(
                chat_id=message.chat.id, 
                from_chat_id=Config.QUICK_REPLY, 
                message_id=msg.id, 
                schedule_date=schedule_time,
            ) 
    except Exception as e:
        print(e)
    

@Client.on_message(filters.regex(r"Payment Details kerala") & filters.private & filters.incoming)
async def send_qr_quick(client, message):
    QR = [11, 12]
    try:
        for ms_id in QR:
            schedule_time = datetime.now() + timedelta(seconds=5)
            await client.copy_message(
                chat_id=message.chat.id, 
                from_chat_id=Config.QUICK_REPLY, 
                message_id=ms_id, 
                schedule_date=schedule_time,
            ) 
    except Exception as e:
        print(e)
        

@Client.on_message(filters.photo & filters.private & filters.incoming)          
async def get_ss(c, m):
    try:
        user = await c.get_users(m.chat.id)
        caption = f"""User: {user.mention}
Id: `{user.id}`        
Username: {user.username}
Name: {user.first_name} {user.last_name if user.last_name else ''}

User Sended Payment"""

        buttons = [[
            InlineKeyboardButton('✔️ ᴀᴄᴄᴇᴩᴛ', callback_data=f'verify+{user.id}')
            ],[
            InlineKeyboardButton('❌ ʀᴇᴊᴇᴄᴛ', callback_data=f'reject+{user.id}')
        ]]
        msg = await m.copy(chat_id=Config.V_CHANNEL, caption=caption)
        await c.bot.edit_message_reply_markup(
            chat_id=Config.V_CHANNEL,
            message_id=msg.id,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await c.bot.send_message(chat_id=Config.V_CHANNEL, text=e)


           
        
