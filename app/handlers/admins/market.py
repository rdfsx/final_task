from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import quote_html, hbold
from odmantic import AIOEngine

from app.keyboards.reply import CancelMarkup
from app.models import ProductModel
from app.states.admin_states import AdminGoods


async def adding_goods_title(m: Message):
    await AdminGoods.TITLE.set()
    await m.answer("Введи название товара:", reply_markup=CancelMarkup().get())


async def adding_goods_description(m: Message, state: FSMContext):
    await AdminGoods.DESCRIPTION.set()
    await state.update_data(title=quote_html(m.text))
    await m.answer("Хорошо, пришли описание товара, например: что можно с ним сделать или насколько он полезен",
                   reply_markup=CancelMarkup().get())


async def adding_goods_price(m: Message, state: FSMContext):
    await AdminGoods.PRICE.set()
    await state.update_data(description=quote_html(m.text))
    await m.answer("Принято! Введи цену товара в долларах, для отделения дробной части используй точку",
                   reply_markup=CancelMarkup().get())


async def adding_goods_photo(m: Message, state: FSMContext):
    try:
        price = float(m.text)
    except ValueError:
        return await m.answer("Ты ввёл цену в неверном формате! Введи цену ЧИСЛОМ:", reply_markup=CancelMarkup().get())
    await AdminGoods.PHOTO.set()
    await state.update_data(price=price)
    await m.answer("Хорошо, последний шаг: отправь фото")


async def save_goods(m: Message, state: FSMContext, db: AIOEngine):
    data = await state.get_data()
    product = ProductModel(title=data.get("title"),
                           description=data.get("description"),
                           price=data.get("price"),
                           photo=m.photo[-1].file_id)
    await db.save(product)
    await state.reset_state()
    await m.answer("Готово! Вот, что получилось:")
    await m.answer_photo(product.photo, "\n\n".join(
        [
            hbold(product.title),
            product.description,
            f"${product.price}",
        ]
    ), reply_markup=None)


def setup(dp: Dispatcher):
    dp.register_message_handler(adding_goods_title, commands="add_goods", is_admin=True)
    dp.register_message_handler(adding_goods_description, state=AdminGoods.TITLE, is_admin=True)
    dp.register_message_handler(adding_goods_price, state=AdminGoods.DESCRIPTION, is_admin=True)
    dp.register_message_handler(adding_goods_photo, state=AdminGoods.PRICE, is_admin=True)
    dp.register_message_handler(save_goods, state=AdminGoods.PHOTO, content_types=types.ContentType.PHOTO,
                                is_admin=True)
