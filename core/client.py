"""Pyrogram bot client wrapper with lifecycle management."""
from typing import Optional
from pyrogram import Client
from pyrogram.types import User
from config import Config
from core.logger import setup_logger
from core.database import Database

logger = setup_logger(__name__)


class BotClient:
    """Wrapper around Pyrogram Client for better lifecycle management."""

    def __init__(self):
        """Initialize bot client."""
        self.client: Optional[Client] = None
        self.me: Optional[User] = None
        self.db = Database()

    async def start(self) -> None:
        """Start bot client and connect to database."""
        try:
            # Connect to database
            await self.db.connect()
            logger.info("Database connection initialized")

            # Create and start client
            self.client = Client(
                name="FileToLinkBot",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=Config.BOT_TOKEN,
                workers=Config.WORKERS,
                no_updates=False,
            )

            await self.client.start()
            self.me = await self.client.get_me()

            logger.info(f"✅ Bot Started Successfully!")
            logger.info(f"Bot Username: @{self.me.username}")
            logger.info(f"Bot Name: {self.me.first_name}")
            logger.info(f"Bot ID: {self.me.id}")

        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise

    async def stop(self) -> None:
        """Stop bot client and disconnect from database."""
        try:
            if self.client:
                await self.client.stop()
                logger.info("Bot client stopped")

            await self.db.disconnect()
            logger.info("Database disconnected")
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")

    def get_client(self) -> Client:
        """Get the Pyrogram client instance."""
        if not self.client:
            raise RuntimeError("Bot client not started")
        return self.client

    def get_database(self) -> Database:
        """Get the database instance."""
        return self.db
