from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from odmantic import AIOEngine, ObjectId

from app.constants.product import get_product_text
from app.keyboards.inline import ShowGoodsKb
from app.models import ProductModel


async def get_goods(inline: InlineQuery, db: AIOEngine):
    limit = 20
    offset = 0 if inline.offset == '' else int(inline.offset)
    results = []
    data = await db.find(ProductModel, limit=limit, skip=offset)
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
                    reply_markup=await ShowGoodsKb().get(product.id, product.price),
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
    await inline.answer(results=results, next_offset=next_offset, cache_time=10)


async def change_amount(q: CallbackQuery, db: AIOEngine, callback_data: dict):
    await q.answer()
    action = callback_data['@']
    product = await db.find_one(ProductModel, ProductModel.id.eq(ObjectId(callback_data['goods_id'])))
    actual_amount = int(q.message.reply_markup.inline_keyboard[0][0].values.get('text'))
    new_amount = actual_amount + 1 if action == 'add_goods' else actual_amount - 1
    if new_amount < 1:
        new_amount = actual_amount
    await q.message.edit_reply_markup(
        await ShowGoodsKb().get(
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
