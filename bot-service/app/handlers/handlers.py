import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.state import PwdState, City
from app.filter import IsRita
from app.config import DATE
from app.images.img_manager import get_photo_file, cache_photo_file_id
from app.app_logging import logger

from app.kb import kb
from app.loader import redis_client as redis
from app.config import ADMIN_ID

from app import config

ids = []


router = Router()

@router.message(CommandStart())
async def start_for_rita(message: Message, state: FSMContext, bot: Bot):
    await message.answer('🔐 Напишите дату начала последних отношений в формате dd.mm.yyyy\n<i>Например 01.11.2011</i>', parse_mode='HTML')
    logger.info(f"В бот зашел: {message.from_user.full_name}, id:{message.from_user.id}, username:{message.from_user.username}\n\n")
    await bot.send_message(chat_id=ADMIN_ID, text=f"В бот зашел: {message.from_user.full_name}, id:{message.from_user.id}, username:{message.from_user.username}\n\n")

    await state.set_state(PwdState.date)


@router.message(PwdState.date)
async def check_date(message: Message, state: FSMContext, bot: Bot):
    date_to_chek = message.text
    if date_to_chek == DATE:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Авторизацию прошёл: {message.from_user.full_name}, id:{message.from_user.id}, username:{message.from_user.username}\n\n")
        await state.clear()
        ids.append(message.from_user.id)
        await message.answer("❤️‍🔥 <b>Это точно Рита</b>", parse_mode='HTML')

        photo = await get_photo_file(redis, "./app/images/welcome.jpeg")
        msg = await message.answer_photo(photo=photo)
        await cache_photo_file_id(redis, msg, "./app/images/welcome.jpeg")

        await message.answer(text=config.HELLO_TEXT, reply_markup=kb.start_kb(), parse_mode='HTML')

        return
    await message.answer('❌ либо вы ошиблись в дате, либо бот предназначен не для вас')


@router.callback_query(IsRita(ids), F.data == 'start_questions')
async def start_questions(call: CallbackQuery, state: FSMContext):
    photo = await get_photo_file(redis, "./app/images/rita_ufa.png")
    msg = await call.message.answer_photo(photo=photo)
    await cache_photo_file_id(redis, msg, "./app/images/rita_ufa.png")
    await call.message.answer(text='🌆 <i>Напиши название города, в котором было сделано это фото (с большой буквы)</i>', parse_mode='HTML')
    await state.set_state(City.city_name)


@router.message(IsRita(ids), City.city_name)
async def check_city_name(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    city = message.text
    if city == 'Уфа':
        text = '🎯 <i>Да это реально было в Уфе</i>'
    else:
        text = '<b>Это было в уфе</b>🥺'
    await message.answer(text=text, parse_mode='HTML')
    await bot.send_message(chat_id=ADMIN_ID, text=f"Выбрал город {city}: {message.from_user.full_name}, id:{message.from_user.id}, username:{message.from_user.username}\n\n")

    photo = await get_photo_file(redis, "./app/images/richi_woman.png")
    msg = await message.answer_photo(photo=photo)
    await cache_photo_file_id(redis, msg, "./app/images/richi_woman.png")
    await message.answer(text='🐈 <i>С этой аватаркой связан один твой питомец в прошлом, как его зовут?</i>', reply_markup=kb.pet_kb(), parse_mode='HTML')


@router.callback_query(IsRita(ids), F.data.startswith('pet:'))
async def pet_check(call: CallbackQuery, bot: Bot, state: FSMContext):
    pet = call.data.split('pet:')[1]
    await bot.send_message(chat_id=ADMIN_ID, text=f"Выбрал имя {pet}: {call.from_user.full_name}, id:{call.from_user.id}, username:{call.from_user.username}\n\n")
    if pet == 'Арчи':
        text = '<i>Ты была близка... Его звали Ричи</i>'
    elif pet == 'Ричи':
        text = "<b>Именно так, этого каскадера звали ричи✨</b>"
    else:
        text = "<b>Хоть его и звали Ричи, думаю это имя подходит ему куда больше😜</b>"
    
    await call.message.answer('❌ Неправильный ответ. Свидание отменено')
    await asyncio.sleep(3)
    await call.message.answer('Шучу')
    await asyncio.sleep(1)
    await call.message.answer(text=text, parse_mode='HTML')

    photo_1 = await get_photo_file(redis, "./app/images/photo_1.jpg")
    photo_2 = await get_photo_file(redis, "./app/images/photo_2.jpg")
    await call.message.answer_media_group(media=[
        InputMediaPhoto(media=photo_1),
        InputMediaPhoto(media=photo_2)
    ])
    
    await call.message.answer(text='🎞 <i>Какая из этих фото точно должна оказаться в семейном альбоме?</i>', reply_markup=kb.photo_kb(), parse_mode='HTML')
    

@router.callback_query(IsRita(ids), F.data.startswith('photo:'))
async def check_photo(call: CallbackQuery, bot: Bot):
    num = int(call.data.split('photo:')[1])
    if num == 1:
        text = "<b>Эту фотку точно пересматривать будем лет через 30😜</b>"
        joke = ""
    else:
        text = "<i>Нуууу.. Эта фотка тоже хороша)</i>"

    await call.message.answer(text=text, parse_mode='HTML')

    await bot.send_message(chat_id=ADMIN_ID, text=f"Выбрал фото {num}: {call.from_user.full_name}, id:{call.from_user.id}, username:{call.from_user.username}\n\n")

    await call.message.answer(text='🤵‍♂️ Это было бы очень бестактно с моей стороны не позволить тебе выбрать время, поэтому скажи, во сколько тебе было бы удобнее', reply_markup=kb.choose_time_kb())


@router.callback_query(IsRita(ids), F.data.startswith('time:'))
async def choose_time(call: CallbackQuery, bot: Bot):
    time = call.data.split('time:')[1]
    text = f'<b>✅ Отлично, тогда 4.11 (вт) примерно в {time}:00 за тобой подъедет такси</b>\n\nБудь на связи в это время, включи уведомления на бота, здесь появится номер машины, так же тебе отправится ближе к этому времени сообщение с вопросом готовности'
    await call.message.answer(text=text, parse_mode='HTML')

    await bot.send_message(chat_id=ADMIN_ID, text=f"Выбрал время {time}:00 : {call.from_user.full_name}, id:{call.from_user.id}, username:{call.from_user.username}\n\n")


@router.callback_query(IsRita(ids), F.data.startswith('ready:'))
async def choose_time(call: CallbackQuery, bot: Bot):
    time = call.data.split('ready:')[1]
    text = f"<i>✅ Отлично, когда будешь готова - нажми  кнопку 'Я готова'</i>"
    await call.message.answer(text=text, parse_mode='HTML')

    await bot.send_message(chat_id=ADMIN_ID, text=f"Будет готова через {time}: минут {call.from_user.full_name}, id:{call.from_user.id}, username:{call.from_user.username}\n\n")