from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, BIN_CHANNEL, PROTECT_CONTENT, FSUB, FSUB_CHANNEL, LOG_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    
    # Force Subscribe Check (if enabled)
    if FSUB and FSUB_CHANNEL:
        try:
            member = await client.get_chat_member(FSUB_CHANNEL, user_id)
            if member.status in ["kicked", "left"]:
                await message.reply_text("⚠️ Please join the channel first to use this bot.")
                return
        except:
            pass
    
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
            except Exception as e:
                await message.reply_text(f"❌ File not found or expired.\n\nError: {str(e)}")
            return
        
        # Batch link (will add later)
        elif data.startswith("batch_"):
            await message.reply_text("📦 Batch feature coming soon!")
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
        )
    
    await message.reply_text(help_text)

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    user_id = message.from_user.id
    
    help_text = (
        "**📚 How to use:**\n\n"
        "**For Single File:**\n"
        "1. Send me any file\n"
        "2. Get a shareable link\n"
        "3. Share with anyone!\n\n"
        "**Features:**\n"
        "• Permanent file storage\n"
        "• Fast file delivery\n"
        "• Easy sharing\n"
    )
    
    await message.reply_text(help_text)

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMINS))
async def stats(client, message):
    await message.reply_text(
        "**📊 Bot Statistics**\n\n"
        "Bot is running successfully!\n"
        "Database stats will be added soon."
    )
