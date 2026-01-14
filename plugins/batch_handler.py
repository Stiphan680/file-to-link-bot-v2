from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import BIN_CHANNEL, PROTECT_CONTENT
from database.batch_db import batch_db
import asyncio

async def send_batch_files(client, user_id, batch_id):
    # Get batch data
    batch = await batch_db.get_batch(batch_id)
    
    if not batch:
        await client.send_message(user_id, "❌ Batch not found or expired.")
        return
    
    batch_data = batch['batch_data']
    files = batch_data['files']
    total_files = batch_data['count']
    
    # Send status message
    status_msg = await client.send_message(
        user_id,
        f"📦 **Batch Download Started!**\n\n"
        f"Total Files: {total_files}\n"
        f"Please wait while I send all files..."
    )
    
    # Send all files
    sent_count = 0
    failed_count = 0
    
    for file_info in files:
        try:
            file_id = file_info['file_id']
            
            # Get message from BIN_CHANNEL
            msg = await client.get_messages(BIN_CHANNEL, file_id)
            
            # Send to user
            await msg.copy(
                chat_id=user_id,
                protect_content=PROTECT_CONTENT
            )
            
            sent_count += 1
            
            # Update status every 5 files
            if sent_count % 5 == 0:
                await status_msg.edit_text(
                    f"📦 **Sending Batch Files...**\n\n"
                    f"Progress: {sent_count}/{total_files}\n"
                    f"Please wait..."
                )
            
            # Small delay to avoid flood
            await asyncio.sleep(1)
            
        except FloodWait as e:
            # Handle flood wait
            await asyncio.sleep(e.value)
            # Retry
            try:
                await msg.copy(
                    chat_id=user_id,
                    protect_content=PROTECT_CONTENT
                )
                sent_count += 1
            except:
                failed_count += 1
                
        except Exception as e:
            failed_count += 1
            continue
    
    # Final status
    await status_msg.edit_text(
        f"✅ **Batch Download Complete!**\n\n"
        f"📦 Total Files: {total_files}\n"
        f"✅ Sent: {sent_count}\n"
        f"❌ Failed: {failed_count}"
    )

# Register handler in start.py (will be called from there)
