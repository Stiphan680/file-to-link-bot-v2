from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import ADMINS, BIN_CHANNEL, PROTECT_CONTENT, FSUB, FSUB_CHANNEL, LOG_CHANNEL
from utils import get_size

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    
    # Force Subscribe Check
    if FSUB and FSUB_CHANNEL:
        try:
            member = await client.get_chat_member(FSUB_CHANNEL, user_id)
            if member.status in ["kicked", "left"]:
                await message.reply_text("Please join the channel first to use this bot.")
                return
        except:
            await message.reply_text("Please join the channel first to use this bot.")
            return
    
    # Add user to database
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        if LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"New User: {message.from_user.mention} - {user_id}")
    
    # Handle deep links
    if len(message.command) > 1:
        data = message.command[1]
        
        # Single file link
        if data.startswith("file_"):
            file_id = int(data.split("_")[1])
            try:
                msg = await client.get_messages(BIN_CHANNEL, file_id)
                await msg.copy(
                    chat_id=user_id,
                    protect_content=PROTECT_CONTENT
                )
            except:
                await message.reply_text("File not found or expired.")
            return
    
    # Default start message
    await message.reply_text(
        f"Hello {message.from_user.mention}!\n\n"
        "I'm a file to link bot. Send me any file and I'll give you a shareable link.\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/stats - Get stats (Admin only)"
    )

@Client.on_message(filters.command("help") & filters.private)
async def help(client, message):
    await message.reply_text(
        "**How to use:**\n\n"
        "1. Send me any file (document, video, audio, photo)\n"
        "2. I'll store it and give you a shareable link\n"
        "3. Anyone with the link can access the file\n\n"
        "**Features:**\n"
        "- Permanent file storage\n"
        "- Fast file delivery\n"
        "- Easy sharing"
    )

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def stats(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"**Bot Statistics**\n\nTotal Users: {total_users}")
