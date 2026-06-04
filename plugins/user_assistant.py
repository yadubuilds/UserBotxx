import asyncio, os, sys, datetime, pytz, time, re, logging

from helper.utils import get_date_for_contact
from pyrogram import Client, filters, enums
from datetime import timedelta, datetime
from helper.database import db
from config import Config, Txt
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
 

@Client.on_bot_business_message(filters.command("link") & filters.private & filters.user(97874787))
async def send_link(c, m):
    try:
        id = int(m.text.split(' ', 1)[1])
        chat_id = Config.GROUPS[id]
    except Exception as e:
        return await m.edit(e)
    try:
        user = m.from_user
        chat = await c.User.get_chat(chat_id)
        link = await c.User.create_chat_invite_link(int(chat_id), member_limit=1)
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
        
    await m.edit(f"Kidungamani ULTRA welcomes you\n\n**{chat.title}**\n\n\n{link.invite_link}", disable_web_page_preview=True)
 


IN_MSG = r"""Kerala Group 😍"""

# Quick Reppy
@Client.on_bot_business_message(filters.regex(IN_MSG) & filters.private & filters.incoming)
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
    

@Client.on_bot_business_message(filters.regex(r"Payment Details kerala") & filters.private & filters.incoming)
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
        

@Client.on_bot_business_message(filters.photo & filters.private & filters.incoming)          
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
        await c.edit_message_reply_markup(
            chat_id=Config.V_CHANNEL,
            message_id=msg.id,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await c.send_message(chat_id=Config.V_CHANNEL, text=e)


           
        
