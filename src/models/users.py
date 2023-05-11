import uuid

from src import db
from src.models.enums import SexEnum
from src.models.tables import clients_pets
from src.routers.password import get_password_hash


class UsersModel(db.Model):
    __tablename__ = "users"

    # Обязательные параметры
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(254), nullable=False)

    # Необязательные параметры
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.Enum(SexEnum), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(36), unique=True)

    # Очень внимательно следить за lazy, чтобы уйти от проблемы N + 1 запрос
    pets = db.relationship("PetsModel", secondary=clients_pets, lazy="subquery",
                           backref=db.backref("users", lazy=True))

    # init для создания uuid и хеширования пароля
    def __init__(self, email, password, firstname=None, lastname=None,
                 phone=None, sex=None, birthdate=None, is_admin=False):
        # Обязательные параметры
        self.email = email
        self.password = get_password_hash(password)

        # Необязательные параметры
        self.firstname = firstname.capitalize() if firstname else firstname
        self.lastname = lastname.capitalize() if lastname else lastname
        self.phone = phone
        self.sex = sex
        self.birthdate = birthdate
        self.is_admin = is_admin
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Clients(email={self.email}, firstname={self.firstname}, id={self.id}, pets={self.pets})"
