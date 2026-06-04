from helper.utils import humanbytes, get_time
from pyrogram import Client, filters, enums
from pyrogram.types import * 
from helper.database import db
from config import Config, Txt
    
import re, asyncio, time, os, sys, shutil, psutil



@Client.on_message(filters.command('group_settings') & filters.private & filters.user(Config.ADMINS))
async def group_settings(client, message):
    groups = await db.list_groups()
    
    button = []
    for grp in groups:
        button.append([InlineKeyboardButton(grp['title'], callback_data=f"group+{grp['_id']}")])
        
    button.append([InlineKeyboardButton('➕ ADD GROUP ➕', callback_data="add_group")])
    
    await message.reply("Its your group settings", reply_markup=InlineKeyboardMarkup(button))
    
    
    
@Client.on_callback_query()
async def group_settings_cb(client, query):
    data = query.data
    message = query.message
    user_id = query.from_user.id
    
    
    if data == "add_group":
        ask = await message.reply('Ok. Send Group Id. Must Add me & userbot in the group.  id like  `-100xxxxx`')     
        group_id = await client.wait_for_message(user_id, filters=filters.text)
        await ask.delete()
        
        if group_id.text.startswith("/"):
            await message.edit("**ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!**")
            return await group_id.continue_propagation()

        group_id = int(group_id.text)
        try:
            group = await client.get_chat(group_id)
        except Exception as e:
            return await message.edit(f"**error!: {e}**")
            
        title_ask = await message.reply('Ok. Send Group Title')  
        title = await client.wait_for_message(user_id, filters=filters.text)
        await title_ask.delete()
        
        if title.text.startswith("/"):
            await message.edit("**ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!**")
            return await title.continue_propagation()

        title = title.text
        
        
        price_ask = await message.reply('Ok. Send Group Price 💵')  
        price = await client.wait_for_message(user_id, filters=filters.text)
        await price_ask.delete()
        
        if price.text.startswith("/"):
            await message.edit("**ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ!**")
            return await price.continue_propagation()

        price = int(price.text)
        await db.add_group(group_id, title, price)
        
        await message.edit(f"Successfully added `{group_id}` ({title})  with {price}₹ ✓. /group_settings to manage")
      
    elif data.startswith('group'):
        ident, key = data.split('+')
        grp = await db.get_group(key)
        if grp:
            txt = (
                f"Group Name: `{grp['title']}`\n"
                f"Group Id: `{grp['group_id']}`\n"
                f"Price: `{grp['price']}`₹\n"
                f"Created At: {grp['created_at']}\n"
                f"Group Key: {grp['_id']}"
            )
            btn = [[
                InlineKeyboardButton('edit id', f"idedit+{grp['_id']}"),
                InlineKeyboardButton('edit title', f"titleedit+{grp['_id']}")
                ],[
                InlineKeyboardButton('edit price', f"priceedit+{grp['_id']}")
            ]]
            await message.edit(text=txt, reply_markup=InlineKeyboardMarkup(btn))
        
    else:
        raise ContinuePropagation    
        
        
        