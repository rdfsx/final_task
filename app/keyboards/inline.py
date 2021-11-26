from aiogram.utils.callback_data import CallbackData
from aiogram.utils.deep_linking import get_start_link

from app.utils.markup_constructor import InlineMarkupConstructor


class ExampleInlineMarkup(InlineMarkupConstructor):
    callback_data = CallbackData('test', 'number')

    def get(self):
        schema = [3, 2, 1]
        actions = [
            {'text': '1', 'callback_data': self.callback_data.new('1')},
            {'text': '2', 'callback_data': self.callback_data.new('2')},
            {'text': '3', 'callback_data': '3'},
            {'text': '4', 'callback_data': self.callback_data.new('4')},
            {'text': '5', 'callback_data': (self.callback_data, '5')},
            {'text': '6', 'callback_data': '6'},
        ]
        return self.markup(actions, schema)


class CancelKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Отмена', 'cb': 'cancel'},
        ]
        return self.markup(actions, schema)


class CancelAndDeleteKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Отмена', 'cb': 'cancel_delete'},
        ]
        return self.markup(actions, schema)


class MarketFinishKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Отмена', 'cb': 'cancel'},
        ]
        return self.markup(actions, schema)


class EditGoodsKb(InlineMarkupConstructor):
    anew = "anew_goods"
    save = "save_goods"

    def get(self):
        actions = [
            {'text': 'Заполнить заново', 'cb': self.anew},
            {'text': "Сохранить", 'cb': self.save}
        ]
        return self.markup(actions, [1] * len(actions))


class ShowGoodsKb(InlineMarkupConstructor):
    add_goods_data = CallbackData("add_goods", "goods_id", "amount")
    remove_goods_data = CallbackData("remove_goods", "goods_id", "amount")
    buy_goods_data = CallbackData("buy_goods", "goods_id", "amount")

    async def get(self, goods_id: str, price: float, amount: int = 1, is_start: bool = False):
        schema = [1, 1, 2, 1]
        actions = [
            {'text': f'{amount}', 'cb': 'pass'},
            {'text': f"Цена: ${round(price * amount, 1)}", 'cb': 'pass'},
            {'text': '➕', 'cb': self.add_goods_data.new(goods_id, amount + 1)},
            {'text': '➖', 'cb': 'pass' if amount == 1 else self.remove_goods_data.new(
                goods_id, amount - 1 if amount > 1 else 1
            )},
        ]
        if not is_start:
            actions.append({'text': 'Показать товар', 'url': await get_start_link(f'good_id-{goods_id}-{amount}')})
        else:
            actions.append({'text': 'Купить', 'cb': self.buy_goods_data.new(goods_id, amount)})
        return self.markup(actions, schema)
