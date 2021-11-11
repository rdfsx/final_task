from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import hide_link
from odmantic import AIOEngine, ObjectId

from app.models import UserModel, ProductModel


async def get_start_message(m: Message, db: AIOEngine):
    if (args := m.get_args()) and (product := await db.find_one(
            ProductModel, ProductModel.id.eq(ObjectId(args.replace("good_id-", ""))))
    ):
        return await m.answer(
            f'<b>Товар:</b> {product.title}\n\n'
            f'<b>Описание:</b> {product.description}'
            f'{hide_link(product.photo_url)}\n\n'
            f'<b>Цена:</b> ${product.price}'
        )
    await m.answer(f"Привет, {m.from_user.first_name}!")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_start_message, commands="start")
