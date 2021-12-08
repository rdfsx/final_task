import json
from datetime import datetime

from beanie import before_event, Insert, Replace, SaveChanges
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

    @before_event([Insert, Replace, SaveChanges])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()
