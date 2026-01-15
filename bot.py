#!/usr/bin/env python3
"""Main bot entry point with new architecture."""

import asyncio
import sys
from threading import Thread
from aiohttp import web

from config import Config
from core import BotClient, setup_logger
from handlers.start import start_handler  # noqa: F401

# Setup logging
logger = setup_logger("FileToLinkBot")


class HealthCheckServer:
    """Health check web server for Render deployment."""

    def __init__(self, port: int = 8080):
        """Initialize health check server.
        
        Args:
            port: Port to run the server on
        """
        self.port = port
        self.runner = None

    async def health_check(self, request) -> web.Response:
        """Health check endpoint."""
        return web.Response(text="Bot is running! ✅")

    async def start(self) -> None:
        """Start the health check server."""
        app = web.Application()
        app.router.add_get("/", self.health_check)
        app.router.add_get("/health", self.health_check)

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, Config.HOST, self.port)
        await site.start()
        logger.info(f"✅ Health check server started on port {self.port}")

    async def stop(self) -> None:
        """Stop the health check server."""
        if self.runner:
            await self.runner.cleanup()


async def main() -> None:
    """Main bot function."""
    # Validate configuration
    try:
        Config.validate()
        logger.info("✅ Configuration validated")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(1)

    # Initialize bot client
    bot = BotClient()

    # Initialize health check server
    health_server = HealthCheckServer(port=Config.PORT)

    try:
        logger.info("="*60)
        logger.info("🚀 Starting File to Link Bot...")
        logger.info("="*60)

        # Start health check server in background
        logger.info("Starting health check server...")
        health_task = asyncio.create_task(health_server.start())

        # Start bot
        logger.info("Starting Telegram bot...")
        await bot.start()

        # Keep bot running
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await asyncio.sleep(float('inf'))

    except KeyboardInterrupt:
        logger.info("\n🛑 Shutdown signal received")
    except Exception as e:
        logger.error(f"❌ FATAL ERROR: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Shutting down...")
        await bot.stop()
        await health_server.stop()
        logger.info("✅ Bot stopped gracefully")


if __name__ == "__main__":
    # For local development
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
