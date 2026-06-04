from pyrogram import Client, filters

# Disable sharing command
@Client.on_message(filters.command("protect", ".") & filters.me)
async def disable_sharing(client, message):
    chat_id = message.chat.id

    try:
        await client.set_chat_protected_content(chat_id, True)
        await message.edit("🔒 Sharing Disabled in this chat")
    except Exception as e:
        await message.edit(f"Error: {e}")


# Enable sharing again
@Client.on_message(filters.command("unprotect", ".") & filters.me)
async def enable_sharing(client, message):
    chat_id = message.chat.id

    try:
        await client.set_chat_protected_content(chat_id, False)
        await message.edit("✅ Sharing Enabled")
    except Exception as e:
        await message.edit(f"Error: {e}")
