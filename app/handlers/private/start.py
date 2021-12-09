from aiogram import Dispatcher
from aiogram.types import Message
from beanie import PydanticObjectId

from app.constants.product import get_product_text
from app.keyboards.inline import ShowGoodsKb
from app.models import ProductModel


async def get_product(m: Message):
    args = m.get_args()
    if product := await ProductModel.get(PydanticObjectId(args.replace("good_id-", "").split("-")[0])):
        return await m.answer(get_product_text(product),
                              reply_markup=await ShowGoodsKb().get(
                                  str(product.id),
                                  product.price,
                                  int(args.replace("good_id-", "").split("-")[1])),
                              )


async def get_start_message(m: Message,):
    await m.answer(f"Привет, {m.from_user.first_name}!")


def setup(dp: Dispatcher):
    dp.register_message_handler(get_product, lambda m: m.get_args() != '', commands="start")
    dp.register_message_handler(get_start_message, commands="start")
