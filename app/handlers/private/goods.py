from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from odmantic import AIOEngine

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
                    description=f"${product.price}, {product.description}",
                    input_message_content=InputTextMessageContent(product.title + product.description),
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
    await inline.answer(results=results, next_offset=next_offset)


def setup(dp: Dispatcher):
    dp.register_inline_handler(get_goods)
