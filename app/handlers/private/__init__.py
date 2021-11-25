from aiogram import Dispatcher

from app.handlers.private import default, start, help_, goods, order


def setup(dp: Dispatcher):
    for module in (start, goods, order, default, help_):
        module.setup(dp)
