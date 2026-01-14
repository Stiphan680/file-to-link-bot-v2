# File to Link Bot

A simple Telegram bot that converts files to shareable links.

## Features

- Upload any file and get a permanent shareable link
- Simple and clean interface
- Fast file delivery
- MongoDB database for tracking

## Setup

### Required Environment Variables

```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
ADMINS=your_user_id
DATABASE_URI=mongodb_connection_string
DATABASE_NAME=filetolinkbot
BIN_CHANNEL=channel_id_for_storing_files
LOG_CHANNEL=channel_id_for_logs
```

### Optional Variables

```
PROTECT_CONTENT=True  # Enable content protection
FSUB=True  # Enable force subscribe
FSUB_CHANNEL=-100xxx  # Channel ID for force subscribe
```

## Deploy on Render

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create New Web Service
4. Connect your GitHub repository
5. Select Docker runtime
6. Add all environment variables
7. Deploy!

## Commands

- `/start` - Start the bot
- `/help` - Get help
- `/stats` - Get statistics (Admin only)

## How it works

1. User sends a file to the bot
2. Bot stores it in BIN_CHANNEL
3. Bot generates a unique link
4. User shares the link
5. Anyone with the link can access the file

## License

MIT
