import asyncio
import sys
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN

# Validate environment variables
if not API_ID or API_ID == 0:
    print("ERROR: API_ID is not set!")
    sys.exit(1)

if not API_HASH:
    print("ERROR: API_HASH is not set!")
    sys.exit(1)

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN is not set!")
    sys.exit(1)

print(f"Starting bot with API_ID: {API_ID}")

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileToLinkBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"},
            workers=4
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"Bot Started: @{me.username}")
        print(f"Bot ID: {me.id}")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped!")

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
