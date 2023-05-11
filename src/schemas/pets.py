from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy.fields import Nested

from src.models.pets import PetsModel
from src.models.enums import TypeEnum, BreedEnum, SexEnum


# Создание схемы для валидации данных по модели
class SPets(SQLAlchemyAutoSchema):
    animal_type = EnumField(TypeEnum, by_value=True)
    sex = EnumField(SexEnum, by_value=True)
    breed = EnumField(BreedEnum, by_value=True)

    class Meta:
        model = PetsModel
        # exclude = ["id"]
        load_instance = True
        include_fk = True

    # Добавлять ли ссылку на users в отображении
    # users = Nested("SUsers", many=True, exclude=("pets",))

