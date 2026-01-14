from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import ADMINS, BIN_CHANNEL, PROTECT_CONTENT, FSUB, FSUB_CHANNEL, LOG_CHANNEL
from utils import get_size
from plugins.batch_handler import send_batch_files

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    
    # Force Subscribe Check
    if FSUB and FSUB_CHANNEL:
        try:
            member = await client.get_chat_member(FSUB_CHANNEL, user_id)
            if member.status in ["kicked", "left"]:
                await message.reply_text("⚠️ Please join the channel first to use this bot.")
                return
        except:
            await message.reply_text("⚠️ Please join the channel first to use this bot.")
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
                await message.reply_text("❌ File not found or expired.")
            return
        
        # Batch link
        elif data.startswith("batch_"):
            batch_id = data.split("_")[1]
            await send_batch_files(client, user_id, batch_id)
            return
    
    # Default start message
    help_text = (
        f"Hello {message.from_user.mention}! 👋\n\n"
        "I'm a file to link bot. Send me any file and I'll give you a shareable link.\n\n"
        "**Commands:**\n"
        "• /start - Start the bot\n"
        "• /help - Get help\n"
    )
    
    if user_id in ADMINS:
        help_text += (
            "\n**Admin Commands:**\n"
            "• /stats - Get bot statistics\n"
            "• /batch - Create batch (multiple files in one link)\n"
            "• /done - Finish batch creation\n"
            "• /cancel - Cancel batch\n"
        )
    
    await message.reply_text(help_text)

@Client.on_message(filters.command("help") & filters.private)
async def help(client, message):
    user_id = message.from_user.id
    
    help_text = (
        "**📚 How to use:**\n\n"
        "**For Single File:**\n"
        "1. Send me any file\n"
        "2. Get a shareable link\n"
        "3. Share with anyone!\n\n"
    )
    
    if user_id in ADMINS:
        help_text += (
            "**For Batch (Multiple Files):**\n"
            "1. Send /batch command\n"
            "2. Send all files one by one\n"
            "3. Send /done when finished\n"
            "4. Get ONE link for ALL files!\n\n"
            "**Example Use Cases:**\n"
            "• Study materials (all PDFs in one link)\n"
            "• Course videos (all lectures together)\n"
            "• Notes collection (organized chapters)\n"
        )
    
    await message.reply_text(help_text)

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def stats(client, message):
    total_users = await db.total_users_count()
    await message.reply_text(f"**📊 Bot Statistics**\n\nTotal Users: {total_users}")
