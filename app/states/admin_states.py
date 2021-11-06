from aiogram.dispatcher.filters.state import StatesGroup, State


class AnswerAdmin(StatesGroup):
    ANSWER = State()


class BroadcastAdmin(StatesGroup):
    BROADCAST = State()


class AdminGoods(StatesGroup):
    GOODS = State()


class AdminEditGoods(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    PHOTO = State()
    PRICE = State()
