import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.bot_loader import bot, dp
from app.app_logging import logger  # просто импорт активирует конфиг

async def run_bot(bot: Bot, dp: Dispatcher):
    logger.info("🚀 Бот запущен и готов к работе")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot(bot, dp))
    except (KeyboardInterrupt, SystemExit):
        logger.warning("🛑 Бот остановлен пользователем")