import asyncio
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import quote_html, hbold
from odmantic import AIOEngine

from app.keyboards.inline import CancelKb, EditGoodsKb, CancelAndDeleteKb
from app.keyboards.reply import MarketMarkup
from app.models import ProductModel
from app.states.admin_states import AdminGoods, AdminEditGoods


async def add_goods(ctx: Union[Message, CallbackQuery], state: FSMContext):
    if isinstance(ctx, types.CallbackQuery):
        msg = ctx.message
        await state.reset_state()
        await ctx.answer()
        await ctx.message.delete()
    else:
        msg = ctx
    await msg.answer("Чтобы добавить товар, пришлите его фото со следующим описанием:")
    await asyncio.sleep(2)
    await msg.answer("\n\n".join(
        [
            "Название",
            "Описание",
            "Цена в долларах",
        ]
    ), reply_markup=CancelKb().get())
    await AdminGoods.GOODS.set()


async def get_photo_failed(m: Message):
    await m.answer("Сообщение нужно отправить с фото! Попробуй ещё раз.", reply_markup=CancelKb().get())


async def final_goods(m: Message, state: FSMContext):
    text = m.caption.split()
    if len(text) != 3:
        return await m.answer("Неверный формат текста: строк должно быть ровно три. Пришли ещё раз.",
                              reply_markup=CancelKb().get())
    try:
        price = float(text[2])
    except ValueError:
        return await m.answer("Ты ввёл цену в неверном формате! Цену нужно вводить числом.",
                              reply_markup=CancelKb().get())
    photo = m.photo[-1].file_id
    title = text[0]
    description = text[1]
    await state.update_data(photo=photo, title=title, description=description, price=price)
    await state.reset_state(False)
    await m.answer("Готово! Вот, что получилось:")
    await m.answer_photo(photo, "\n\n".join(
        [
            hbold(title),
            description,
            f"${price}",
        ]
    ), reply_markup=EditGoodsKb().get())


async def save_goods(query: CallbackQuery, state: FSMContext, db: AIOEngine):
    await query.answer()
    await query.message.edit_reply_markup()
    data = await state.get_data()
    product = ProductModel(title=data.get("title"),
                           description=data.get("description"),
                           price=float(data.get("price")),
                           photo=data.get("photo"))
    await db.save(product)
    await state.reset_state()
    await query.message.answer("Товар сохранён.")


def setup(dp: Dispatcher):
    dp.register_message_handler(add_goods, commands="add_goods", is_admin=True)
    dp.register_callback_query_handler(add_goods, text=EditGoodsKb.anew, is_admin=True)
    dp.register_message_handler(final_goods, state=AdminGoods.GOODS,
                                content_types=types.ContentType.PHOTO, is_admin=True)
    dp.register_message_handler(get_photo_failed, state=AdminGoods.GOODS, is_admin=True)
    dp.register_callback_query_handler(save_goods, text=EditGoodsKb.save, is_admin=True)
