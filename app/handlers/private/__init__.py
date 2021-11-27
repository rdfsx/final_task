from aiogram import Dispatcher

from app.handlers.private import default, start, help_, goods, order, buying


def setup(dp: Dispatcher):
    for module in (start, goods, buying, order, default, help_):
        module.setup(dp)
