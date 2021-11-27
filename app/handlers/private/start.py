from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import hide_link
from odmantic import AIOEngine, ObjectId

from app.constants.product import get_product_text
from app.keyboards.inline import ShowGoodsKb
from app.models import UserModel, ProductModel


async def get_product(m: Message, db: AIOEngine):
    args = m.get_args()
    if product := await db.find_one(
            ProductModel, ProductModel.id.eq(ObjectId(args.replace("good_id-", "").split("-")[0]))):
        return await m.answer(get_product_text(product),
                              reply_markup=await ShowGoodsKb().get(
                                  product.id,
                                  product.price,
                                  int(args.replace("good_id-", "").split("-")[1]),
                                  True),
                              )


async def get_start_message(m: Message,):
    await m.answer(f"Привет, {m.from_user.first_name}!")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_product, lambda m: m.get_args() != '', commands="start")
    dp.register_message_handler(get_start_message, commands="start")
