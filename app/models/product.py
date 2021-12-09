from pydantic import Field

from app.models.base import TimeBaseModel


class ProductModel(TimeBaseModel):
    title: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    photo_id: str = Field(...)
    photo_width: int = Field(...)
    photo_height: int = Field(...)
    photo_url: str = Field(...)

    class Collection:
        name = "Products"
