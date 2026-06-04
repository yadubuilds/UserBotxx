import asyncio, os, sys, datetime, pytz, time, re

from config import Config, Txt
from helper.database import db
from pyrogram import Client, filters, enums
from pyrogram.types import *

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    if len(message.command) != 1:
        if message.command[1].startswith('Member_'):
            user_id = message.from_user.id
            key = message.command[1].split('Member_')[1]
            print(key)
            check = await db.check_user(user_id, key)
            if check == "True":
                data = await db.get_user(user_id)
                group_id = int(data['group_id'])
                try: link = await client.create_chat_invite_link(group_id, member_limit=1) 
                except: return await message.reply("I Can't Create The Link 🥲 Maybe I am Not Admin In This Group. Make Me Admin") 
                await message.reply(f"Do not left 🫦\n\nHere Is Your Link: {link.invite_link}\n⚠️One Time Link")    
            else:
                await message.reply(f"Hey {message.from_user.full_name}\n\n{check}", quote=True)
        return 
    
    
    btn = [[
        KeyboardButton("📞 𝗦𝗵𝗮𝗿𝗲 𝗖𝗼𝗻𝘁𝗮𝗰𝘁", request_contact=True)
        ],[
        KeyboardButton("𝗔𝗗𝗠𝗜𝗡 ✅"),
        KeyboardButton("𝗢𝗙𝗙𝗘𝗥 🎁")
        ],[
        KeyboardButton("🔰 𝗔𝗹𝗹 𝗟𝗲𝗮𝗸 𝗖𝗼𝗹𝗹𝗲𝗰𝘁𝗶𝗼𝗻"),
        KeyboardButton("🔰 𝗩𝗜𝗣 𝗠𝗲𝗺𝗯𝗲𝗿")
        ],[
        KeyboardButton("🔰 𝗡𝗼𝗿𝗺𝗮𝗹 𝗚𝗿𝗼𝘂𝗽"),
        KeyboardButton("🔰 𝗠𝗮𝗹𝗹𝘂 𝗢𝗻𝗹𝘆")
        ],[
        KeyboardButton("✘ 𝗖𝗹𝗼𝘀𝗲")
    ]]
    photos = [InputMediaPhoto(pic) for pic in Config.PICS]
    # for index, group_id in enumerate(Config.GROUPS):
    #     try: chat = await client.get_chat(group_id)
    #     except: continue
    #     btn.append([InlineKeyboardButton(chat.title, f"group_{index}")])
        
    keyboard = ReplyKeyboardMarkup(
        btn,
        one_time_keyboard=True,
        resize_keyboard=True
    )
    send = await message.reply_media_group(media=photos, quote=True)
    await send[0].edit(Txt.START_TEXT.format(message.from_user.full_name)) #, reply_markup=keyboard)
    await message.reply('Select Group', reply_markup=keyboard)
    
    
@Client.on_message(filters.regex('✘ 𝗖𝗹𝗼𝘀𝗲') & filters.private)
async def close_keyboard_markup(client, message):
    s = await message.reply_text("Keyboard closed.", reply_markup=ReplyKeyboardRemove())
    await s.delete()
    await message.delete()

    

