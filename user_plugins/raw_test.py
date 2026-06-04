import logging
from pyrogram import Client, filters
from pyrogram.raw import functions, types, base

@Client.on_message(filters.command('online') & filters.user('self'))
async def send_if_online(client, message):
    chat_id = message.chat.id
    await message.delete()
    try:
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            functions.messages.SendMessage(
                peer=peer,
                message="hello",
                # background=True, 
                random_id=client.rnd_id(),
                quick_reply_shortcut=types.InputQuickReplyShortcutId(shortcut_id=7),
            )
        )
    except Exception as e:
        await message.reply(e)