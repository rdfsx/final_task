import asyncio
import logging
from typing import Union

import aiofiles.os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, CallbackQuery

from app.keyboards.reply import MarketMarkup
from app.models import UserModel


async def get_amount_users(m: Message):
    amount = await UserModel.count()
    await m.answer(f"Количество пользователей в базе данных: {amount}")


async def get_exists_users(m: Message):
    await m.answer("Начинаем подсчет...")
    bot = m.bot
    users = await UserModel.find_all().to_list()
    count = 0
    for user in users:
        try:
            if await bot.send_chat_action(user.id, "typing"):
                count += 1
        except Exception as e:
            logging.exception(e)
        await asyncio.sleep(.05)
    await m.answer(f"Активных пользователей: {count}")


async def write_users_to_file(m: Message):
    await m.answer("Начинаем запись...")
    users = await UserModel.find_all().to_list()
    filename = 'users.txt'
    async with aiofiles.open(filename, mode='w') as f:
        for user in users:
            await f.write(f"{user.id}\n")
    await m.answer_document(InputFile(filename))
    await aiofiles.os.remove(filename)


async def cancel_all(ctx: Union[CallbackQuery, Message], state: FSMContext):
    await state.reset_state()
    msg = ctx
    if isinstance(ctx, CallbackQuery):
        await ctx.answer()
        msg = ctx.message
        await msg.delete()
    await msg.answer('Отменено.')


async def cancel_delete(ctx: Union[CallbackQuery, Message], state: FSMContext):
    await state.reset_state(False)
    if isinstance(ctx, CallbackQuery):
        await ctx.answer()
        msg = ctx.message
        await msg.delete()


def setup(dp: Dispatcher):
    dp.register_message_handler(get_amount_users, commands="amount", is_admin=True)
    dp.register_message_handler(get_exists_users, commands="exists_amount", is_admin=True)
    dp.register_message_handler(write_users_to_file, commands="users_file", is_admin=True)
    dp.register_callback_query_handler(cancel_all, text='cancel', state='*', is_admin=True)
    dp.register_callback_query_handler(cancel_delete, text='cancel_delete', is_admin=True)
    dp.register_message_handler(cancel_all, text=MarketMarkup.cancel_text, state='*', is_admin=True)
