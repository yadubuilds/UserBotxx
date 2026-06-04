from helper.utils import humanbytes, get_time
from pyrogram import Client, filters, enums
from helper.database import db
from config import Config, Txt
    
import re, asyncio, time, os, sys, shutil, psutil


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMINS) & filters.private)
async def status_handler(client, message):
    total, used, free = shutil.disk_usage(".")
    ram = psutil.virtual_memory()
    start_t = time.time()
    sts = await message.reply_text("ᴡᴀɪᴛ..")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    total_users = await db.total_users_count()

    stats = Txt.STATS.format(
        uptime = get_time(time.time() - client.uptime),
        ping = f"{time_taken_s:.3f} ᴍꜱ",
        total = humanbytes(total),
        used = humanbytes(used),
        free = humanbytes(free),
        t_ram = humanbytes(ram.total),
        u_ram = humanbytes(ram.used),
        f_ram = humanbytes(ram.available),
        cpu_usage = psutil.cpu_percent(),
        ram_usage = psutil.virtual_memory().percent,
        disk_usage = psutil.disk_usage('/').percent,
        total_users = total_users,
        sent = humanbytes(psutil.net_io_counters().bytes_sent),
        recv = humanbytes(psutil.net_io_counters().bytes_recv),
    )
    await sts.edit(stats, parse_mode=enums.ParseMode.MARKDOWN) 


@Client.on_message(filters.command("restart") & filters.user(Config.ADMINS))
async def restart_bot(client, message):
    await message.reply("Rᴇꜱᴛᴀᴛɪɴɢ........")
    try: os.remove('log.txt')
    except: pass 
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("update") & filters.user(Config.ADMINS))
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
