import asyncio, os, sys, datetime, pytz, time, re

from config import Config, Txt
from helper.database import db
from pyrogram import Client, filters, enums, ContinuePropagation
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait



@Client.on_callback_query()
async def cb_handler(client, cb):
    data = cb.data
    if data == "close":
        await cb.message.delete() 
        
    elif data.startswith('verify'):
        user_id = int(data.split('+', 1)[1])

        user = await client.User.get_users(user_id)
        caption = f"""Link Sended ✅
        
User: {user.mention}
Id: `{user.id}`        
Username: {user.username}
Name: {user.first_name} {user.last_name if user.last_name else ''}"""

        await cb.message.edit(caption)
        try:
            await client.User.send_message(user_id, "Link")
        except Exception as e:
            return await cb.answer(e, show_alert=True)
        
        return await cb.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton('ᴠᴇʀɪꜰɪᴇᴅ ✅', 'dummy')]]))
       
    elif data.startswith('reject'):
        uid = int(data.split('+', 1)[1])
        try:
            await client.User.send_message(uid, "Send Original Screen Shot Bro. Its Fake")
        except Exception as e:
            return await cb.answer(e, show_alert=True)
            
        user = await client.User.get_users(uid)
        caption = f"""Rejected ✘
        
User: {user.mention}
Id: `{user.id}`        
Username: {user.username}
Name: {user.first_name} {user.last_name if user.last_name else ''}"""    
        await cb.message.edit(caption)
        await cb.edit_message_reply_markup(InlineKeyboardMarkup([[InlineKeyboardButton('ʀᴇᴊᴇᴄᴛᴇᴅ ❌', 'dummy')]]))
       
    else:
        raise ContinuePropagation