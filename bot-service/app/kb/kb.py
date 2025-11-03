from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Начать', callback_data="start_questions")

    return kb.as_markup()


def pet_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='💼 Арчи', callback_data='pet:Арчи')
    kb.button(text='💸 Ричи', callback_data='pet:Ричи')
    kb.button(text='😈 Рыжий дебил', callback_data='pet:Рыжий')

    return kb.as_markup()


def photo_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='1', callback_data='photo:1')
    kb.button(text='2', callback_data='photo:2')

    return kb.as_markup()


def choose_time_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='17:00', callback_data="time:17")
    kb.button(text='18:00', callback_data="time:18")
    kb.button(text='19:00', callback_data="time:19")
    kb.button(text='20:00', callback_data="time:20")
    kb.adjust(2,2)

    return kb.as_markup()


def are_u_ready_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='💅 Я готова', callback_data="ready:0")
    kb.button(text='15', callback_data="ready:15")
    kb.button(text='30', callback_data="ready:30")
    kb.button(text='45', callback_data='ready:45')
    kb.button(text='60', callback_data="ready:60")
    kb.adjust(1, 2, 2)

    return kb.as_markup()
    
