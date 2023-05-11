from datetime import datetime, timedelta

import jwt
from flask import request, make_response
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src import db, app
from src.models.users import UsersModel
from src.routers.password import verify_password
from src.schemas.users import SUsers


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Api только для регистрации пользователей
class AuthRegisterApi(Resource):
    user_schema = SUsers()

    @classmethod
    def post(cls):
        # Попытка валидации данных
        try:
            user = cls.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400
        # Попытка добавления записи пользователя, тут может быть ошибка
        # Из-за не уникальности email
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {"message": str(e)}, 409
        return {"message": cls.user_schema.dump(user)}, 201


class AuthLoginApi(Resource):
    auth_scheme = SUsers()

    @classmethod
    def post(cls):
        # Попытка валидации данных
        try:
            user = cls.auth_scheme.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400

        email = request.json["email"]
        password = request.json["password"]

        # Получаем пользователя
        user = db.session.query(UsersModel).filter_by(email=email).first()

        # Проверяем наличие пользователя в БД по данному email
        if not user:
            return {"message": f"Пользователь c почтой '{email}' не найден"}, 404

        # Проверяем корректность пароля
        elif not verify_password(password, user.password):
            return {"message": f"Не верно указан пароль - '{password}' "}, 400

        # Генерируем JWT токен длительностью на 1 час
        access_token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.now() + timedelta(hours=1)
            },
            app.config['JWT_KEY'],
            app.config["JWT_ALGORITHMS"]
        )

        # Добавим jwt токен в cookies и дополнительно еще в ответе
        # Если токен нужен CURL или отдать через фронт пользователю
        response = make_response({"access_token": access_token}, 200)
        response.set_cookie('access_token', access_token, httponly=True)
        return response


class AuthLogoutApi(Resource):

    @classmethod
    def get(cls):
        resp = make_response({"message": "Токен удален"})
        resp.set_cookie('access_token', expires=0)
        return resp
