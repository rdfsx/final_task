from aiogram import Dispatcher, types
from aiogram.types import Message, ShippingQuery, PreCheckoutQuery, LabeledPrice

from app.models.sale_item import SaleItem

Tesla_S = SaleItem(
    title="Tesla Model S",
    description="Tesla Model S — пятидверный электромобиль производства американской компании Tesla. "
                "Прототип был впервые показан на Франкфуртском автосалоне в 2009 году; "
                "поставки автомобиля в США начались в июне 2012 года",
    currency="USD",
    prices=[
        LabeledPrice(
            label="Тесла Model S",
            amount=560
        )
    ],
    start_parameter="create_invoice_tesla_model_s",
    photo_url="https://static-assets.tesla.com/configurator/compositor?&options=$MTS12,$PPSW,$WS10,$IBE00&view=FRONT34&model=ms&size=1920&bkba_opt=1&version=v0028d202111110422&crop=1300,500,300,300&version=v0028d202111110422",
    photo_width=841,
    photo_height=323,
)

Tesla_X = SaleItem(
    title="Tesla Model X",
    description="Tesla Model X — полноразмерный электрический кроссовер производства компании Tesla. "
                "Прототип был впервые показан в Лос-Анджелесе 9 февраля 2012 года. "
                "Коммерческие поставки начались 29 сентября 2015 года. "
                "Tesla Model X разрабатывается на базе платформы "
                "Tesla Model S и собирается на основном заводе компании во Фримонте, штат Калифорния.",
    currency="RUB",
    prices=[
        LabeledPrice(
            label="Tesla",
            amount=35_000_00
        ),
        LabeledPrice(
            label="Доставка",
            amount=15_000_00
        ),
        LabeledPrice(
            label="Скидка",
            amount=-5_000_00
        ),
        LabeledPrice(
            label="НДС",
            amount=10_000_00
        ),
    ],
    need_shipping_address=True,
    start_parameter="create_invoice_tesla_model_x",
    photo_url="https://static-assets.tesla.com/configurator/compositor?&options=$MTX12,$PPSW,$WX20,$IBE00&view=FRONT34&model=mx&size=1920&bkba_opt=1&version=v0028d202111110422&crop=1300,600,300,230&version=v0028d202111110422",
    photo_width=841,
    photo_height=388,
    is_flexible=True
)

POST_REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Почтой',
    prices=[
        types.LabeledPrice(
            'Обычная коробка', 0),
        types.LabeledPrice(
            'Почтой обычной', 1000_00),
    ]
)
POST_FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Почтой (vip)',
    prices=[
        types.LabeledPrice(
            'Супер прочная коробка', 1000_00),
        types.LabeledPrice(
            'Почтой срочной - DHL (3 дня)', 3000_00),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(id='pickup',
                                       title='Самовывоз',
                                       prices=[
                                           types.LabeledPrice('Самовывоз из магазина', -100_00)
                                       ])


async def show_invoices(m: Message):
    await m.bot.send_invoice(chat_id=m.from_user.id, **Tesla_S.generate_invoice(), payload="123456")
    await m.bot.send_invoice(chat_id=m.from_user.id, **Tesla_X.generate_invoice(), payload="123457")


async def choose_shipping(query: ShippingQuery):
    if query.shipping_address.country_code == "UA":
        await query.bot.answer_shipping_query(shipping_query_id=query.id,
                                              shipping_options=[
                                                  POST_FAST_SHIPPING,
                                                  POST_REGULAR_SHIPPING,
                                                  PICKUP_SHIPPING],
                                              ok=True)
    elif query.shipping_address.country_code == "US":
        await query.bot.answer_shipping_query(shipping_query_id=query.id,
                                              ok=False,
                                              error_message="Сюда не доставляем")
    else:
        await query.bot.answer_shipping_query(shipping_query_id=query.id,
                                              shipping_options=[POST_REGULAR_SHIPPING],
                                              ok=True)


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    bot = pre_checkout_query.bot
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Спасибо за покупку! Ожидайте отправку")


def setup(dp: Dispatcher):
    dp.register_message_handler(show_invoices, commands=["invoices"])
    dp.register_shipping_query_handler(choose_shipping)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
