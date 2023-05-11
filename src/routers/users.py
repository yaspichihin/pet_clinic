from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src import db
from src.models.pets import PetsModel
from src.models.users import UsersModel
from src.routers.decorators import check_token_and_give_admin_status_and_uuid
from src.schemas.users import SUsers


class UsersApi(Resource):
    users_schema = SUsers()

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def get(cls, user_is_admin, user_uuid, value: int | str | None = None):

        # Вернуть всех клиентов клиники, если фамилия и id не указаны
        # И пользователь является администратором
        if value is None and user_is_admin:
            users = db.session.query(UsersModel).all()
            return {"message": cls.users_schema.dump(users, many=True)}, 200

        # Вернуть запись самого пользователя, если фамилия и id не указаны
        # И пользователь не является администратором
        if value is None and not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid).first()
            return {"message": cls.users_schema.dump(user)}, 200

        # Вернуть клиента клиники по указанному id из всех пользователей
        # Если пользователь администратор
        if type(value) == int and user_is_admin:
            user = db.session.query(UsersModel).filter_by(id=value).first()
            if user:
                return {"message": cls.users_schema.dump(user)}, 200
            return {"message": f"Клиент по указанному id '{value}' не найден"}, 404

        # Вернуть самого пользователя по-указанному своему id, если id не совпадает, то 404
        # Если пользователь не администратор
        if type(value) == int and not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid, id=value).first()
            if user:
                return {"message": cls.users_schema.dump(user)}, 200
            return {"message": f"Клиент по указанному id '{value}' не найден"}, 404

        # Вернуть список пользователей, которые соответствуют искомой фамилии
        # Доступ только для администраторов
        if type(value) == str and user_is_admin:
            # Вернуть клиентов клиники по указанной фамилии
            users = db.session.query(UsersModel).filter_by(lastname=value.capitalize())
            users = cls.users_schema.dump(users, many=True)
            if users:
                return {"message": users}, 200
            # Вернуть сообщение об ошибке и 404 код если клиент не найден
            return {"message": f"Клиент по указанной фамилии '{value}' не найден"}, 404
        if type(value) == str and not user_is_admin:
            return {"message": "Поиск клиентов по фамилий доступен только для администраторов"}, 403

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def post(cls, user_is_admin, user_uuid):
        if user_is_admin:
            try:
                user = cls.users_schema.load(request.json, session=db.session)
            except (ValidationError, IntegrityError) as e:
                return {"message": str(e)}, 400
            try:
                db.session.add(user)
                db.session.commit()
                return {"message": cls.users_schema.dump(user)}, 201
            except IntegrityError as e:
                db.session.rollback()
                return {"message": str(e)}, 409
        return {"message": "Добавление пользователей разрешено только для администраторов"}, 403

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def put(cls, user_is_admin, user_uuid, value: int):
        # Доступ на обновление всех данных пользователей
        # Если пользователь администратор
        if user_is_admin:
            user = db.session.query(UsersModel).filter_by(id=value).first()
            if not user:
                return {"message": f"Клиент с данным id '{value}' не найден"}, 404
            try:
                user = cls.users_schema.load(request.json, instance=user, session=db.session)
            except ValidationError as e:
                return {"message": str(e)}, 400
            try:
                db.session.add(user)
                db.session.commit()
                return {"message": cls.users_schema.dump(user)}, 200
            except IntegrityError as e:
                db.session.rollback()
                return {"message": str(e)}, 409

        # Доступ на обновление только своих данных пользователя
        # Если пользователь не администратор
        if not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid, id=value).first()
            if not user:
                return {"message": f"Клиент с данным id '{value}' не найден"}, 404
            try:
                user = cls.users_schema.load(request.json, instance=user, session=db.session)
            except ValidationError as e:
                return {"message": str(e)}, 400
            try:
                db.session.add(user)
                db.session.commit()
                return {"message": cls.users_schema.dump(user)}, 200
            except IntegrityError as e:
                db.session.rollback()
                return {"message": str(e)}, 409

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def delete(cls, user_is_admin, user_uuid, value: int):
        if user_is_admin:
            # Получить клиента по id
            client = db.session.query(UsersModel).filter_by(id=value).first()
            # Удалить клиента, если он найден
            if client:
                db.session.delete(client)
                db.session.commit()
                return {"message": "Deleted successfully"}, 204
            # Вернуть сообщение об ошибке и 404 код если клиент не найден
            return {"message": f"Клиент с данным id '{value}' не найден"}, 404
        return {"message": "Удаление пользователей разрешено только для администраторов"}, 403


class BindApi(Resource):

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def put(cls, user_is_admin, user_uuid):
        if user_is_admin:
            user_id = request.json["user_id"]
            pet_id = request.json["pet_id"]

            user = db.session.query(UsersModel).filter_by(id=user_id).first()
            pet = db.session.query(PetsModel).filter_by(id=pet_id).first()
            if not user:
                return {"message": f"Пользователь с данным id '{user_id}' не найден"}, 404
            if not pet:
                return {"message": f"Питомец с данным id '{pet_id}' не найден"}, 404

            user_firstname = user.firstname
            pet_name = pet.name

            user.pets.append(pet)
            db.session.commit()
            db.session.close()
            return {"message": f"Пользователю {user_firstname} добавлен питомец '{pet_name}'"}, 200
        return {"message": "Закрепление питомцев разрешено только для администраторов"}, 403

