from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, BIN_CHANNEL, LOG_CHANNEL
from database.files_db import files_db

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_files(client, message):
    user_id = message.from_user.id
    
    # Forward to BIN_CHANNEL
    try:
        forwarded = await message.copy(BIN_CHANNEL)
        file_id = forwarded.id
        
        # Generate shareable link
        bot_username = (await client.get_me()).username
        link = f"https://t.me/{bot_username}?start=file_{file_id}"
        
        # Save to database
        file_name = ""
        if message.document:
            file_name = message.document.file_name
        elif message.video:
            file_name = message.video.file_name or "video.mp4"
        elif message.audio:
            file_name = message.audio.file_name or "audio.mp3"
        
        await files_db.add_file(file_id, user_id, file_name)
        
        # Send link to user
        buttons = [[
            InlineKeyboardButton("🔗 Open Link", url=link)
        ]]
        await message.reply_text(
            f"**File Uploaded Successfully!**\n\n"
            f"📄 File: `{file_name}`\n"
            f"🔗 Link: `{link}`\n\n"
            f"Share this link with anyone to give them access to the file.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        # Log to channel
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"New File Upload\nUser: {message.from_user.mention}\nFile: {file_name}\nID: {file_id}"
            )
    except Exception as e:
        await message.reply_text(f"Error uploading file: {str(e)}")
