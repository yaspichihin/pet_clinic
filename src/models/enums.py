import enum


class TypeEnum(enum.Enum):
    cat = "cat"
    dog = "dog"
    parrot = "parrot"
    ...


class SexEnum(enum.Enum):
    male = "male"
    female = "female"


class BreedEnum(enum.Enum):
    husky = "husky"
    shepherd = "shepherd"
    mongrel = "mongrel"
    ...
