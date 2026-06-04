from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters, enums
from config import Config, Txt

import asyncio, datetime, time, os, sys, logging


@Client.on_chat_join_request() #filters.chat(Config.REQUEST_CHANNEL))
async def req_send(client, message):
    logging.info('req recived')
    
    try: 
        user = await client.User.get_users(message.from_user.id)
        await client.User.set_chat_message_auto_delete_time(chat_id=user.id, message_auto_delete_time=604800)
        logging.info('auto delete time set')
        # await client.User.send_message(user.username, Txt.REQ_TEXT)
    except Exception as e: 
        logging.error(e)
   



