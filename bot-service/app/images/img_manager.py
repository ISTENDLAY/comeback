import asyncio
import os
from aiogram.types import FSInputFile, Message
from app.clients.redis_client import RedisClient
from app.app_logging import logger


async def get_photo_file(redis: RedisClient, photo_path: str, cache_key: str | None = None):
    """
    Возвращает file_id из Redis или FSInputFile, если кэша нет.
    Работает с любыми картинками. Использует блокировку, чтобы избежать гонок.
    :param redis: клиент Redis
    :param photo_path: путь к локальному файлу
    :param cache_key: необязательный ключ кэша (по умолчанию генерируется из имени файла)
    """
    key_base = cache_key or os.path.basename(photo_path)
    file_key = f"photo:{key_base}:file_id"
    lock_key = f"{file_key}:lock"

    # если уже кэшировано
    file_id = await redis.get(file_key)
    if file_id:
        return file_id.decode() if isinstance(file_id, bytes) else file_id

    # если кто-то уже загружает — ждём и пробуем снова
    if await redis.exists(lock_key):
        logger.info(f"Waiting for {key_base} upload to finish...")
        await asyncio.sleep(2)
        file_id = await redis.get(file_key)
        if file_id:
            return file_id.decode() if isinstance(file_id, bytes) else file_id

    # ставим лок, чтобы не дублировать отправку
    await redis.set(lock_key, "1", expires=10)

    # возвращаем путь к файлу — бот сам отправит, и потом закэшируем file_id
    return FSInputFile(photo_path)


async def cache_photo_file_id(redis: RedisClient, message: Message, photo_path: str, cache_key: str | None = None):
    """
    Кэширует file_id после успешной отправки фото.
    Работает с любыми изображениями.
    """
    try:
        if not message.photo:
            logger.warning("No photo found in message to cache.")
            return

        key_base = cache_key or os.path.basename(photo_path)
        file_key = f"photo:{key_base}:file_id"
        lock_key = f"{file_key}:lock"

        file_id = message.photo[-1].file_id
        await redis.set(file_key, file_id)
        await redis.delete(lock_key)
        logger.info(f"✅ Cached file_id for {key_base}: {file_id}")

    except Exception as e:
        logger.error(f"⚠️ Failed to cache file_id for {photo_path}: {e}")