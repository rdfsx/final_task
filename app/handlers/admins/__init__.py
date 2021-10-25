from aiogram import Dispatcher

from app.handlers.admins import broadcast, commands, market


def setup(dp: Dispatcher):
    for module in (broadcast, commands, market):
        module.setup(dp)
