"""Constants and message templates for the bot."""

# ============ Messages ============
WELCOME_MSG = """
👋 **Welcome to File to Link Bot!**

I can convert your files into shareable links.

**Features:**
• Upload files and get permanent links
• Share files securely
• Fast and reliable

**Commands:**
/start - Show this message
/help - Get detailed help
/files - View your uploaded files
/settings - Configure preferences
"""

HELP_MSG = """
💫 **Help & Instructions**

**How to use:**
1. Send me a file (document, video, audio, etc.)
2. I'll upload it to our secure storage
3. You'll get a shareable link

**Commands:**
/start - Welcome message
/help - This message
/files - Your uploaded files
/settings - Change settings
/about - About the bot
/support - Get support

**Supported File Types:**
All file types are supported!
Max size: 2GB (depends on account)
"""

ERROR_MSG = """
❌ **Error Occurred**

Sorry, something went wrong.
Please try again or contact support.

/support - Get help
"""

# ============ Status Messages ============
UPLOADING = "📄 Uploading your file..."
PROCESSING = "⏳ Processing..."
COMPLETED = "✅ Done!"
FAILED = "❌ Failed! Please try again."

# ============ Limits ============
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
MAX_FILES_PER_USER = 100
FILE_EXPIRY_DAYS = 30

# ============ Regex Patterns ============
USER_ID_PATTERN = r"^\d{1,10}$"
CHANNEL_PATTERN = r"^-100?\d{1,19}$"
URL_PATTERN = r"https?://[^\s]+"
