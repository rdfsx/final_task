from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedPhoto
from aiogram.utils.markdown import hide_link
from odmantic import AIOEngine

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
                        message_text=f'<b>Товар:</b> {product.title}\n\n'
                                     f'<b>Описание:</b> {product.description}'
                                     f'{hide_link(product.photo_url)}\n\n'
                                     f'<b>Цена:</b> ${product.price}'
                    ),
                    reply_markup=await ShowGoodsKb().get(product.id),
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


def setup(dp: Dispatcher):
    dp.register_inline_handler(get_goods)
