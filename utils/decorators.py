"""Decorators for handlers (auth, permissions, etc)."""
from functools import wraps
from typing import Callable, Any
from pyrogram import Client
from pyrogram.types import Message
from config import Config
from core.logger import setup_logger

logger = setup_logger(__name__)


def admin_only(func: Callable) -> Callable:
    """Decorator to restrict command to admins only."""
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs) -> Any:
        if message.from_user.id not in Config.ADMINS:
            await message.reply(
                "🚫 You don't have permission to use this command."
            )
            logger.warning(
                f"Unauthorized admin command from {message.from_user.id}"
            )
            return

        return await func(client, message, *args, **kwargs)

    return wrapper


def owner_only(func: Callable) -> Callable:
    """Decorator to restrict command to owner only."""
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs) -> Any:
        if message.from_user.id != Config.OWNER_ID:
            await message.reply(
                "🚫 You don't have permission to use this command."
            )
            logger.warning(
                f"Unauthorized owner command from {message.from_user.id}"
            )
            return

        return await func(client, message, *args, **kwargs)

    return wrapper


def handle_errors(func: Callable) -> Callable:
    """Decorator to handle exceptions in handlers."""
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs) -> Any:
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            try:
                await message.reply(
                    f"💩 **Error:** {str(e)[:100]}"
                )
            except Exception:
                pass

    return wrapper
