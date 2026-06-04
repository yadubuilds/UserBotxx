import logging
from pyrogram import Client, filters
from pyrogram.raw import functions, types


@Client.on_message(filters.command('mkn'))
async def quick_mkn(client, message):
    chat_id = message.chat.id   
    shortcut_id = 7
    try:
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            functions.messages.SendQuickReplyMessages(
                peer=peer,
                shortcut_id=shortcut_id,
                id=[],
                random_id=client.rnd_id(),
            )
        )
    except Exception as e:
        await message.reply(e)
            

@Client.on_message(filters.command('get_quick_replys') & filters.user('self'))
async def get_quick_replys(client, message):
    try:
        quick_replies = await client.invoke(functions.messages.GetQuickReplies(hash=0))

        # Format the output for readability
        if quick_replies.quick_replies:
            response = "Quick Replies:\n\n"
            for qr in quick_replies.quick_replies:
                response += f"`{qr.shortcut_id}` - '{qr.shortcut}'\n\n"
        else:
            response = "No quick replies found."
        await message.reply(response)
    except Exception as e:
        await message.reply(e)