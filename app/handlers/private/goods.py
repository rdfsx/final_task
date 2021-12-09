from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from beanie import PydanticObjectId
from beanie.odm.operators.find.evaluation import RegEx

from app.constants.prices import MAX_PRICE, MIN_PRICE
from app.constants.product import get_product_text
from app.keyboards.inline import ShowGoodsKb
from app.models import ProductModel


async def get_goods(iq: InlineQuery):
    limit = 20
    offset = 0 if iq.offset == '' else int(iq.offset)
    results = []
    print(iq.query)
    db_query = RegEx(
        ProductModel.title, rf"({iq.query})"
    ) or RegEx(
        ProductModel.description, rf"({iq.query})"
    )
    data = await ProductModel.find(db_query, limit=limit, skip=offset).to_list()
    if data:
        for product in data:
            results.append(
                InlineQueryResultArticle(
                    id=str(product.id),
                    title=product.title,
                    thumb_url=product.photo_url,
                    description=f"${product.price}, {product.description}",
                    input_message_content=InputTextMessageContent(
                        message_text=get_product_text(product),
                    ),
                    reply_markup=await ShowGoodsKb().get(str(product.id), product.price),
                )
            )
    else:
        not_found = 'Ничего не найдено'
        results = [
            InlineQueryResultArticle(
                id="not_found",
                title=not_found,
                input_message_content=InputTextMessageContent(not_found),
            )
        ]
    next_offset = str(offset + limit) if len(data) >= limit else ''
    await iq.answer(results=results, next_offset=next_offset, cache_time=10)


async def change_amount(q: CallbackQuery, callback_data: dict):
    product = await ProductModel.get(PydanticObjectId(callback_data['goods_id']))
    new_amount = int(callback_data["amount"])
    if new_amount * product.price > MAX_PRICE:
        return await q.answer("Нельзя больше добавить товара! Цена не может быть выше $10,000")
    await q.answer()
    await q.bot.edit_message_reply_markup(
        chat_id=q.message.chat.id if q.message else None,
        message_id=q.message.message_id if q.message else None,
        inline_message_id=q.inline_message_id,
        reply_markup=await ShowGoodsKb().get(
            callback_data['goods_id'],
            product.price,
            new_amount,
        )
    )


async def pass_button(q: CallbackQuery):
    await q.answer()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(change_amount, ShowGoodsKb.add_goods_data.filter())
    dp.register_callback_query_handler(change_amount, ShowGoodsKb.remove_goods_data.filter())
    dp.register_callback_query_handler(pass_button, text='pass')
    dp.register_inline_handler(get_goods)
