import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = os.getenv("ADMIN_ID")

DATE = os.getenv('DATE')


HELLO_TEXT = (
    "Привет! 👋\n\n"
    "Этот бот — особенный. Он знает секреты… и приглашает тебя на маленький опрос. 🎁✨\n\n"
    "Вспомни рандомные моменты из своей жизни. 😉\n\n"
    "Нажми 'Начать', чтобы узнать больше."
)

REDIS_SERVICE_URL = os.getenv('REDIS_SERVICE_URL')
