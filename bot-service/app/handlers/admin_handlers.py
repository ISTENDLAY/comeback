from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject

from app.filter import IsAdmin
from app.handlers.handlers import ids
from app.kb.kb import are_u_ready_kb


router = Router()


# /start только для админа
@router.message(IsAdmin(), CommandStart())
async def start_for_admin(message: Message):
    await message.answer('Вы админ')


# /car {text}, например: /car уф256х будет через 10 минут
@router.message(IsAdmin(), Command(commands=["car"]))
async def send_car_number(message: Message, command: CommandObject, bot: Bot):
    text = command.args  # вот тут получаем аргумент команды
    if not text:
        await message.answer("⚠️ Нужно указать номер машины, например /car уф256х", parse_mode='HTML')
        return
    for user_id in ids:
        await bot.send_message(chat_id=user_id, text=f'🚖 Такси едет:\n<b>{text}</b>', parse_mode='HTML')

    await message.answer('✅ Успешно разосланы сообщения')


# /ready только для админа
@router.message(IsAdmin(), Command(commands=["ready"]))
async def ask_if_ready(message: Message, bot: Bot):
    for user_id in ids:
        await bot.send_message(chat_id=user_id, text=f'Ты уже готова?\nЕсли нет - выбери, сколько минут тебе нужно', reply_markup=are_u_ready_kb(), parse_mode='HTML')

    await message.answer('✅ Успешно разосланы сообщения')