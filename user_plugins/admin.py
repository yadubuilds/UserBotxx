from helper.utils import humanbytes, get_time
from pyrogram import Client, filters, enums
from helper.database import db
from config import Config, Txt
    
import re, asyncio, time, os, sys, shutil, psutil


@Client.on_message(filters.command("restart") & filters.user('self') & filters.chat('me'))                          
async def restart_bot(client, message):
    await message.reply("Rᴇꜱᴛᴀᴛɪɴɢ........")
    try: os.remove('log.txt')
    except: pass 
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("update") & filters.user('self') & filters.chat('me'))
async def update_bot(client, message):
    try:
        try: os.remove('log.txt')
        except: pass 
        os.system("git pull")
        if len(message.command) != 1:
            os.system("pip install -r requirements.txt --force-reinstall")
        await message.reply_text("ᴜᴩᴅᴀᴛᴇᴅ & ʀᴇꜱᴛᴀʀᴛɪɴɢ...")
        os.execl(sys.executable, sys.executable, "bot.py")
    except Exception as e:
        await message.reply(e)
