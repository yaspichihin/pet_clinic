from src import db
from src.models.enums import TypeEnum, SexEnum, BreedEnum


class PetsModel(db.Model):
    __tablename__ = "pets"

    # Обязательные параметры
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.Enum(TypeEnum), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Необязательные параметры
    birthdate = db.Column(db.Date, nullable=True)
    sex = db.Column(db.Enum(SexEnum), nullable=True)
    breed = db.Column(db.Enum(BreedEnum), nullable=True)

    def __init__(self, animal_type, name, birthdate, sex, breed):
        self.animal_type = animal_type
        self.name = name.capitalize()
        self.birthdate = birthdate
        self.sex = sex
        self.breed = breed

    def __repr__(self):
        return f"Pets(animal_type={self.animal_type.value}, name={self.name})"
