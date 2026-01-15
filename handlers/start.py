"""Start command handler."""
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.constants import WELCOME_MSG
from utils.decorators import handle_errors
from core.logger import setup_logger

logger = setup_logger(__name__)


@Client.on_message(filters.command(["start"]))
@handle_errors
async def start_handler(client: Client, message: Message) -> None:
    """Handle /start command."""
    user = message.from_user
    
    # Log user interaction
    logger.info(f"User {user.id} started the bot")
    
    # Send welcome message
    await message.reply(
        WELCOME_MSG,
        disable_web_page_preview=True,
    )
