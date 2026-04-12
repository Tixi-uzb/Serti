import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.fsm.storage.memory import MemoryStorage

import config
import database as db
import user_handlers
import admin_handlers

logging.basicConfig(level=logging.INFO)

async def handle(request):
    return web.Response(text="Bot is running!")

async def dummy_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Dummy web server started on port {port}")

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Initialize the database
    db.create_tables()

    # Include routers
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    # Start dummy web server
    await dummy_web_server()

    # Start the bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
