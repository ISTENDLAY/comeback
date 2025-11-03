import logging
import sys

logger = logging.getLogger("bot-service")
logger.setLevel(logging.INFO)
logger.propagate = False  # чтобы логи не дублировались

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# === чтобы aiogram и uvicorn/fastapi писали через тот же формат ===
logging.getLogger("aiogram").handlers = logger.handlers
logging.getLogger("aiogram").setLevel(logging.INFO)

logging.getLogger("aiohttp").handlers = logger.handlers
logging.getLogger("aiohttp").setLevel(logging.WARNING)

logging.getLogger("uvicorn").handlers = logger.handlers
logging.getLogger("uvicorn.access").handlers = logger.handlers

# по желанию — добавить другие библиотеки