from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import quote_html, hbold
from odmantic import AIOEngine

from app.keyboards.inline import CancelKb, EditGoodsKb
from app.keyboards.reply import MarketMarkup
from app.models import ProductModel
from app.states.admin_states import AdminGoods


async def add_goods(m: Message):
    await m.answer("Чтобы добавить товар, пришлите его фото со следующим описанием:")
    await m.answer("")


async def adding_goods_title(_, m: Message):
    await AdminGoods.TITLE.set()
    await m.answer("Введи название товара:", reply_markup=CancelKb().get())


async def adding_goods_description(_, m: Message, state: FSMContext):
    await AdminGoods.next()
    await state.update_data(title=quote_html(m.text))
    await m.answer("Пришли описание товара, например: что можно с ним сделать или насколько он полезен",
                   reply_markup=MarketMarkup().get())


async def adding_goods_price(_, m: Message, state: FSMContext):
    await AdminGoods.next()
    await state.update_data(description=quote_html(m.text))
    await m.answer("Введи цену товара в долларах, для отделения дробной части используй точку",
                   reply_markup=MarketMarkup().get())


async def adding_goods_photo(_, m: Message, state: FSMContext):
    try:
        price = float(m.text)
    except ValueError:
        return await m.answer("Ты ввёл цену в неверном формате! Введи цену ЧИСЛОМ:", reply_markup=MarketMarkup().get())
    await AdminGoods.next()
    await state.update_data(price=price)
    await m.answer("Хорошо, последний шаг: отправь фото")


async def final_goods(_, m: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(photo=m.photo[-1].file_id)
    await AdminGoods.FIN.set()
    await m.answer("Готово! Вот, что получилось:")
    await m.answer_photo(m.photo[-1].file_id, "\n\n".join(
        [
            hbold(data.get("title")),
            data.get("description"),
            f"${data.get('price')}",
        ]
    ), reply_markup=EditGoodsKb().get())


async def save_goods(query: CallbackQuery, state: FSMContext, db: AIOEngine):
    data = await state.get_data()
    product = ProductModel(title=data.get("title"),
                           description=data.get("description"),
                           price=data.get("price"),
                           photo=data.get("photo"))
    await db.save(product)
    await state.reset_state()
    await query.message.answer("Товар сохранён.")


def setup(dp: Dispatcher):
    dp.register_message_handler(adding_goods_title, ContextFilter(), commands="add_goods", is_admin=True)
    dp.register_message_handler(adding_goods_description, ContextFilter(), state=AdminGoods.TITLE, is_admin=True)
    dp.register_message_handler(adding_goods_price, ContextFilter(), state=AdminGoods.DESCRIPTION, is_admin=True)
    dp.register_message_handler(adding_goods_photo, ContextFilter(), state=AdminGoods.PRICE, is_admin=True)
    dp.register_message_handler(final_goods, ContextFilter(), state=AdminGoods.PHOTO,
                                content_types=types.ContentType.PHOTO,
                                is_admin=True)
    dp.register_callback_query_handler(save_goods, text=EditGoodsKb.save, state=AdminGoods.FIN, is_admin=True)
    dp.register_message_handler(adding_goods_title, text=MarketMarkup.back_text, state=AdminGoods.DESCRIPTION)
    dp.register_message_handler(adding_goods_description, text=MarketMarkup.back_text, state=AdminGoods.PRICE)
    dp.register_message_handler(adding_goods_price, text=MarketMarkup.back_text, state=AdminGoods.PHOTO)
    dp.register_message_handler(adding_goods_photo, text=MarketMarkup.back_text, state=AdminGoods.FIN)
