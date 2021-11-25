from aiogram.utils.markdown import hide_link

from app.models import ProductModel


def get_product_text(product: ProductModel) -> str:
    return "\n".join([
        f'<b>Товар:</b> {product.title}\n',
        f'<b>Описание:</b> {product.description}',
        f'{hide_link(product.photo_url)}',
        f'<b>Цена за штуку:</b> ${product.price}',
    ])
