from aiogram import Bot, Dispatcher
from app.handlers.admin_handlers import router as admin_router
from app.handlers.handlers import router 
from app.config import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(
    admin_router,
    router
)