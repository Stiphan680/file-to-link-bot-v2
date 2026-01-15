"""Centralized configuration management for File to Link Bot."""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Main configuration class."""

    # ============ Bot Configuration ============
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # ============ Admin Configuration ============
    ADMINS: List[int] = (
        [int(i) for i in os.environ.get("ADMINS", "").split()]
        if os.environ.get("ADMINS")
        else []
    )
    OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

    # ============ Database Configuration ============
    DATABASE_URI = os.environ.get(
        "DATABASE_URI", "mongodb+srv://username:password@cluster.mongodb.net/"
    )
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "filetolinkbot")
    # Collections
    USERS_COLLECTION = "users"
    FILES_COLLECTION = "files"
    LOGS_COLLECTION = "logs"

    # ============ Channel Configuration ============
    BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "0"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # ============ Feature Toggles ============
    PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False").lower() == "true"
    FSUB_ENABLED = os.environ.get("FSUB", "False").lower() == "true"
    FSUB_CHANNEL = (
        int(os.environ.get("FSUB_CHANNEL", "0"))
        if os.environ.get("FSUB_CHANNEL")
        else 0
    )

    # ============ Server Configuration ============
    PORT = int(os.environ.get("PORT", "8080"))
    HOST = os.environ.get("HOST", "0.0.0.0")
    WORKERS = int(os.environ.get("WORKERS", "4"))

    # ============ Feature Timeouts ============
    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "60"))
    UPLOAD_TIMEOUT = int(os.environ.get("UPLOAD_TIMEOUT", "300"))
    FILE_EXPIRY_DAYS = int(os.environ.get("FILE_EXPIRY_DAYS", "30"))

    # ============ Logging Configuration ============
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = "bot.log"

    @classmethod
    def validate(cls) -> bool:
        """Validate all required configuration."""
        required_fields = ["API_ID", "API_HASH", "BOT_TOKEN", "DATABASE_URI"]
        for field in required_fields:
            value = getattr(cls, field)
            if not value or (isinstance(value, int) and value == 0):
                raise ValueError(f"Missing required config: {field}")
        return True
