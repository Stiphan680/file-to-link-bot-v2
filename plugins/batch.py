from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, BIN_CHANNEL
from database.batch_db import batch_db
import json

# Temporary storage for batch files
user_batches = {}

@Client.on_message(filters.command("batch") & filters.user(ADMINS))
async def start_batch(client, message):
    user_id = message.from_user.id
    user_batches[user_id] = []
    await message.reply_text(
        "**📦 Batch Mode Started!**\n\n"
        "Now send me all the files you want to include in this batch.\n\n"
        "When done, send /done to generate the batch link."
    )

@Client.on_message(filters.command("done") & filters.user(ADMINS))
async def finish_batch(client, message):
    user_id = message.from_user.id
    
    if user_id not in user_batches or not user_batches[user_id]:
        await message.reply_text("❌ No batch in progress. Use /batch to start.")
        return
    
    batch_files = user_batches[user_id]
    batch_count = len(batch_files)
    
    if batch_count == 0:
        await message.reply_text("❌ No files added to batch. Send files before using /done.")
        return
    
    # Create batch data
    batch_data = {
        "files": batch_files,
        "count": batch_count
    }
    
    # Save to database and get batch_id
    batch_id = await batch_db.create_batch(user_id, batch_data)
    
    # Generate batch link
    bot_username = (await client.get_me()).username
    batch_link = f"https://t.me/{bot_username}?start=batch_{batch_id}"
    
    # Clear temporary storage
    del user_batches[user_id]
    
    # Send batch link
    buttons = [[
        InlineKeyboardButton("🔗 Open Batch Link", url=batch_link)
    ]]
    
    await message.reply_text(
        f"**✅ Batch Created Successfully!**\n\n"
        f"📦 Total Files: {batch_count}\n"
        f"🔗 Batch Link:\n`{batch_link}`\n\n"
        f"Share this link to give access to all {batch_count} files at once!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command("cancel") & filters.user(ADMINS))
async def cancel_batch(client, message):
    user_id = message.from_user.id
    
    if user_id in user_batches:
        del user_batches[user_id]
        await message.reply_text("✅ Batch cancelled.")
    else:
        await message.reply_text("❌ No active batch to cancel.")

@Client.on_message(filters.private & filters.user(ADMINS) & (filters.document | filters.video | filters.audio))
async def collect_batch_files(client, message):
    user_id = message.from_user.id
    
    # Check if user is in batch mode
    if user_id not in user_batches:
        # Not in batch mode, skip
        return
    
    # Forward to BIN_CHANNEL
    try:
        forwarded = await message.copy(BIN_CHANNEL)
        file_id = forwarded.id
        
        # Get file info
        file_name = ""
        file_size = 0
        
        if message.document:
            file_name = message.document.file_name
            file_size = message.document.file_size
        elif message.video:
            file_name = message.video.file_name or "video.mp4"
            file_size = message.video.file_size
        elif message.audio:
            file_name = message.audio.file_name or "audio.mp3"
            file_size = message.audio.file_size
        
        # Add to batch
        user_batches[user_id].append({
            "file_id": file_id,
            "file_name": file_name,
            "file_size": file_size
        })
        
        current_count = len(user_batches[user_id])
        
        await message.reply_text(
            f"✅ File {current_count} added to batch!\n\n"
            f"📄 {file_name}\n\n"
            f"Send more files or use /done to finish."
        )
        
    except Exception as e:
        await message.reply_text(f"❌ Error adding file: {str(e)}")
