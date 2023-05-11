from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy.fields import Nested

from src.models.users import UsersModel
from src.models.enums import SexEnum


# Создание схемы для валидации данных по модели
class SUsers(SQLAlchemyAutoSchema):
    sex = EnumField(SexEnum, by_value=True)

    class Meta:
        model = UsersModel
        exclude = ["is_admin"]
        load_instance = True
        include_fk = True

        # Поля, которые не возвращать после создания
        load_only = ("password",)

    # Должно работать совместно с Nested из SPets, отключил для красоты вывода
    # pets = Nested("SPets", many=True, exclude=("users",))
