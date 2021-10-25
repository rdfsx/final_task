import json
from datetime import datetime

from odmantic import Field, Model


class ProductModel(Model):
    title: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    photo: str = Field(...)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        collection = "Products"
        json_loads = json.loads
        parse_doc_with_default_factories = True
