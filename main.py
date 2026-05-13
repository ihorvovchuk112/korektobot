import asyncio
import logging
import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from handlers import common, text_process

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

logger = logging.getLogger(__name__)

async def main():
    setup_logging()
    
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(common.router, text_process.router)
    
    logger.info("Bot starting...")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")