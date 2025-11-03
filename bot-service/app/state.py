from aiogram.fsm.state import State, StatesGroup

class PwdState(StatesGroup):
    date = State()


class City(StatesGroup):
    city_name = State()