import sys
import asyncio
from threading import Thread
from aiohttp import web
from pyrogram import Client, idle
from info import API_ID, API_HASH, BOT_TOKEN
import os

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
print(f"Bot Token: {BOT_TOKEN[:20]}...")

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
        print(f"✅ Bot Started Successfully!")
        print(f"Bot Username: @{me.username}")
        print(f"Bot Name: {me.first_name}")
        print(f"Bot ID: {me.id}")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped!")

# Health check web server
async def health_check(request):
    return web.Response(text="Bot is running! ✅")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    port = int(os.environ.get('PORT', 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Health check server started on port {port}")
    print(f"URL: http://0.0.0.0:{port}")

def run_health_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_health_server())
    loop.run_forever()

if __name__ == "__main__":
    try:
        # Start health server in separate thread
        print("Starting health check server...")
        health_thread = Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        # Start bot
        print("Starting Telegram bot...")
        bot = Bot()
        bot.run()
        
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
