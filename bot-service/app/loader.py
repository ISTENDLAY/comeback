
from app.config import REDIS_SERVICE_URL

from app.clients.redis_client import RedisClient


redis_client = RedisClient(REDIS_SERVICE_URL)
