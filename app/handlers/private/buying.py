from aiogram import Dispatcher
from aiogram.types import CallbackQuery, LabeledPrice
from beanie import PydanticObjectId

from app.keyboards.inline import ShowGoodsKb
from app.models import ProductModel
from app.models.sale_item import SaleItem


async def buy_goods(q: CallbackQuery, callback_data: dict):
    await q.answer()
    product = await ProductModel.get(PydanticObjectId(callback_data['goods_id']))
    sale_product = SaleItem(
        title=product.title,
        description=product.description,
        currency="USD",
        prices=[
            LabeledPrice(
                label=product.title,
                amount=round(product.price) * int(callback_data["amount"]) * 100
            )
        ],
        start_parameter=f"create_invoice_{product.id}",
        photo_url=product.photo_url,
        photo_width=product.photo_width,
        photo_height=product.photo_height,
    )
    await q.bot.send_invoice(chat_id=q.from_user.id, **sale_product.generate_invoice(), payload=str(product.id))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(buy_goods, ShowGoodsKb.buy_goods_data.filter())
