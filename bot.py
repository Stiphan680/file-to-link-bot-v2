import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileToLinkBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )

    async def start(self):
        await super().start()
        print("Bot Started!")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped!")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
