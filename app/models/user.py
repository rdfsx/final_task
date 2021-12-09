from enum import Enum

from pydantic import Field

from app.models.base import TimeBaseModel


class UserRoles(str, Enum):
    new = 'new'
    user = 'user'
    admin = 'admin'


class UserModel(TimeBaseModel):
    id: int = Field(...)
    language: str = 'en'
    role: UserRoles = Field(default=UserRoles.new)

    class Collection:
        name = "Users"
