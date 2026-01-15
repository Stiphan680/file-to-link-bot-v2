"""Async MongoDB database helper with connection pooling."""
from typing import Optional, Dict, Any, List
import motor.motor_asyncio as motor
from config import Config
from core.logger import setup_logger

logger = setup_logger(__name__)


class Database:
    """Async MongoDB database wrapper."""

    _instance: Optional["Database"] = None
    _client: Optional[motor.AsyncIOMotorClient] = None

    def __new__(cls) -> "Database":
        """Singleton pattern for database connection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            if self._client is None:
                self._client = motor.AsyncIOMotorClient(
                    Config.DATABASE_URI,
                    serverSelectionTimeoutMS=5000,
                )
                # Test connection
                await self._client.admin.command("ping")
                logger.info("✅ Connected to MongoDB")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self._client:
            self._client.close()
            logger.info("Disconnected from MongoDB")

    def get_database(self) -> motor.AsyncIOMotorDatabase:
        """Get database instance."""
        if not self._client:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client[Config.DATABASE_NAME]

    # ============ Users Collection ============
    async def add_user(self, user_id: int, data: Dict[str, Any]) -> None:
        """Add new user to database."""
        db = self.get_database()
        await db[Config.USERS_COLLECTION].update_one(
            {"_id": user_id},
            {"$set": data},
            upsert=True,
        )
        logger.debug(f"User {user_id} added/updated")

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data."""
        db = self.get_database()
        return await db[Config.USERS_COLLECTION].find_one({"_id": user_id})

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        db = self.get_database()
        return await db[Config.USERS_COLLECTION].find({}).to_list(None)

    # ============ Files Collection ============
    async def save_file(self, file_id: str, data: Dict[str, Any]) -> None:
        """Save file metadata."""
        db = self.get_database()
        await db[Config.FILES_COLLECTION].insert_one({"_id": file_id, **data})
        logger.debug(f"File {file_id} saved")

    async def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file metadata."""
        db = self.get_database()
        return await db[Config.FILES_COLLECTION].find_one({"_id": file_id})

    async def get_user_files(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all files from user."""
        db = self.get_database()
        return await db[Config.FILES_COLLECTION].find(
            {"user_id": user_id}
        ).to_list(None)

    # ============ Logs Collection ============
    async def log_action(self, action: str, data: Dict[str, Any]) -> None:
        """Log user action."""
        db = self.get_database()
        from datetime import datetime

        await db[Config.LOGS_COLLECTION].insert_one(
            {"action": action, "timestamp": datetime.utcnow(), **data}
        )
