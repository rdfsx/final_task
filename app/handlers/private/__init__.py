from aiogram import Dispatcher

from app.handlers.private import default, start, help_, goods


def setup(dp: Dispatcher):
    for module in (start, goods, default, help_):
        module.setup(dp)
