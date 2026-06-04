import asyncio, os, sys, datetime, pytz, time, re

from config import Config
from pyrogram import Client, filters
from datetime import timedelta, datetime
from pyrogram.errors import UserNotParticipant

@Client.on_message(filters.command('test') & filters.private & filters.user('self'))                       
async def gen_link(client, message):
    try:
        cmd, id = message.text.split(' ')
        group_id = Config.TEST_GRP[int(id)]  
    except Exception as e:
        return await message.edit(f'ultra error {e}')
    
    try:
        chat = await client.get_chat(group_id)
    except:
        return await message.edit("ultra")
    
    user_id = message.chat.id  
    
    try:
        chat_member = await client.get_chat_member(group_id, user_id)
        if chat_member:
            return await message.edit("You're Already Added")
    except UserNotParticipant:
        pass
    
    try: link = await client.create_chat_invite_link(group_id, member_limit=1) 
    except: return await message.edit("I Can't Create The Link 🥲 Maybe I am Not Admin In This Group. Make Me Admin") 
    
    await message.edit(f"Group 🫦\n\nHere Is Your Link: {link.invite_link}\n⚠️One Time Link")    
                
                
                
#@Client.on_message(filters.new_chat_members & filters.group & filters.chat(Config.TEST_GRP))
async def set_timer(client, message):           
    chat_id = message.chat.id
    for u in message.new_chat_members: 
        text = f"/test_exp {chat_id}"
        schedule_time = datetime.now() + timedelta(minutes=4)
        await client.send_message(chat_id=u.id, text=text, schedule_date=schedule_time)


@Client.on_message(filters.command('test_exp') & filters.private & filters.user('self'))                       
async def test_exp(client, message):
    try:
        cmd, group_id = message.text.split(' ')
        group_id = int(group_id)
        user_id = message.chat.id  
        await client.ban_chat_member(group_id, user_id)
        #await client.unban_chat_member(group_id, user_id)
        msg = await message.edit('Your Trial Time End')
        await message.edit('Your Kidungamani ULTRA Time End. REMOVED')       
    except Exception as e:
        await client.send_message('me', e)
        await message.edit('Your Trial Time End')       
    
    
    
    
    
    
    
    
    
