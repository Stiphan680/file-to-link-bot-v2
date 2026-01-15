# 📁 File to Link Bot v2 - Professional Edition

**A production-ready Telegram bot for converting files into shareable links.**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-green)](https://pyrogram.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Async-green)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🚀 Features

✨ **Core Functionality:**
- Convert files to permanent shareable links
- Support for all file types
- Async/await for better performance
- Real-time logging and monitoring

🔐 **Security & Admin:**
- Admin-only commands with permission checks
- Force subscription (FSUB) support
- Content protection option
- User/action logging to database

📊 **Architecture:**
- Modular design with separated concerns
- Professional error handling
- Database abstraction layer
- Scalable handler system

---

## 📁 Project Structure

```
file-to-link-bot-v2/
├── bot.py                 # Main entry point
├── config.py              # Centralized configuration
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker deployment
│
├── core/
│   ├── client.py          # Bot client wrapper
│   ├── database.py        # Async MongoDB helper
│   └── logger.py          # Logging configuration
│
├── handlers/
│   └── start.py           # Command handlers
│
├── utils/
│   ├── constants.py       # Messages & constants
│   ├── validators.py      # Input validation
│   └── decorators.py      # Permission & error handlers
│
└── .env.example           # Environment template
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11 or higher
- MongoDB (local or cloud)
- Telegram Bot Token
- Telegram API ID & Hash

### Step 1: Clone Repository
```bash
git clone https://github.com/Stiphan680/file-to-link-bot-v2.git
cd file-to-link-bot-v2
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 4: Run Bot
```bash
python bot.py
```

---

## ⚙️ Configuration

### Required Environment Variables

```env
# Bot Configuration
API_ID=123456789
API_HASH="your_api_hash"
BOT_TOKEN="your_bot_token"

# Admin Configuration
OWNER_ID=123456789
ADMINS="123456789 987654321"

# Database
DATABASE_URI="mongodb+srv://..."
DATABASE_NAME="filetolinkbot"

# Channels
BIN_CHANNEL=-100123456789
LOG_CHANNEL=-100123456789

# Features
PROTECT_CONTENT=False
FSUB=False
```

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t file-to-link-bot .
```

### Run Container
```bash
docker run --env-file .env file-to-link-bot
```

### Deploy on Render
1. Push to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy!

---

## 📝 Bot Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/start` | Welcome message | Everyone |
| `/help` | Help & instructions | Everyone |
| `/files` | Your uploaded files | Everyone |
| `/settings` | Change preferences | Everyone |
| `/admin` | Admin panel | Admins only |
| `/stats` | Bot statistics | Admins only |

---

## 💾 Database Models

### Users Collection
```json
{
  "_id": 123456789,
  "username": "john_doe",
  "first_name": "John",
  "files_count": 5,
  "created_at": "2024-01-15"
}
```

### Files Collection
```json
{
  "_id": "file_hash",
  "user_id": 123456789,
  "file_name": "document.pdf",
  "file_size": 1024000,
  "share_link": "https://link.com/xyz123",
  "created_at": "2024-01-15",
  "expires_at": "2024-02-14"
}
```

---

## 🔍 Logging

Logs are saved to `logs/bot.log` with:
- **File Logs:** Full debug information (rotated)
- **Console Logs:** Real-time info level messages
- **Database Logs:** User actions and events

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🆘 Support

- 📧 Email: your-email@example.com
- 💬 Telegram: @YourBotUsername
- 🐛 Issues: [GitHub Issues](https://github.com/Stiphan680/file-to-link-bot-v2/issues)

---

## ⭐ Give it a Star!

If you find this project helpful, please give it a star ⭐!

**Happy Coding! 🚀**
