from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.models.pets import PetsModel
from src.models.users import UsersModel
from src.routers.decorators import check_token_and_give_admin_status_and_uuid
from src.schemas.pets import SPets


class PetsApi(Resource):
    pets_schema = SPets()

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def get(cls, user_is_admin, user_uuid, value: int | str | None = None):

        # Вернуть всех питомцев клиники, если кличка и id питомца
        # не указаны и пользователь является администратором
        if value is None and user_is_admin:
            pets = db.session.query(PetsModel).all()
            return {"message": cls.pets_schema.dump(pets, many=True)}, 200

        # Вернуть всех питомцев только этого пользователя, когда
        # кличка и id питомца не указаны и пользователь не администратор
        if value is None and not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid).first()
            return {"message": cls.pets_schema.dump(user.pets, many=True)}, 200

        # Вернуть любого питомца клиники по-указанному id
        # при условии, что  пользователь является администратором
        if type(value) == int and user_is_admin:
            pet: PetsModel | None = db.session.query(PetsModel).filter_by(id=value).first()
            if pet:
                return {"message": cls.pets_schema.dump(pet)}, 200
            return {"message": f"Питомец по указанному id '{value}' не найден"}, 404

        # Вернуть питомца по-указанному id при условии если питомец
        # принадлежит пользователю и пользователь не является администратором
        if type(value) == int and not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid).first()
            pet: PetsModel | None = db.session.query(PetsModel).filter_by(id=value).first()
            if pet in user.pets:
                return {"message": cls.pets_schema.dump(pet)}, 200
            return {"message": f"Питомец по указанному id '{value}' не найден"}, 404

        # Вернуть всех питомцев клиники по указанной кличке и
        # при условии, что  пользователь является администратором
        if user_is_admin:
            pets = db.session.query(PetsModel).filter_by(name=value.capitalize())
            pets = cls.pets_schema.dump(pets, many=True)
            if pets:
                return {"message": pets}, 200
            return {"message": f"Питомец по указанной кличке '{value}' не найден"}, 404

        # Вернуть питомцев пользователя по указанной кличке и
        # при условии, что  пользователь не является администратором
        if not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid).first()
            pets = [pet for pet in user.pets if pet.name == value.capitalize()]
            pets = cls.pets_schema.dump(pets, many=True)
            if pets:
                return {"message": pets}, 200
            return {"message": f"Питомец по указанной кличке '{value}' не найден"}, 404

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def post(cls, user_is_admin, user_uuid):
        if user_is_admin:
            print(user_uuid)
            try:
                pet = cls.pets_schema.load(request.json, session=db.session)
            except ValidationError as e:
                return {"message": str(e)}, 400
            db.session.add(pet)
            db.session.commit()
            return {"message": cls.pets_schema.dump(pet)}, 201
        return {"message": "Для добавления питомца вы должны быть администратором"}, 403

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def put(cls, user_is_admin, user_uuid, value: int):
        # Доступ на редактирование всех питомцев, если пользователь администратор
        if user_is_admin:
            pet = db.session.query(PetsModel).filter_by(id=value).first()
            if not pet:
                return {"message": f"Питомец с данным id '{value}' не найден"}, 404
            try:
                pet = cls.pets_schema.load(request.json, instance=pet, session=db.session)
            except ValidationError as e:
                return {"message": str(e)}, 400
            db.session.add(pet)
            db.session.commit()
            return {"message": cls.pets_schema.dump(pet)}, 200

        # Доступ на редактирование только своих питомцев, если пользователь не администратор
        if not user_is_admin:
            user = db.session.query(UsersModel).filter_by(uuid=user_uuid).first()
            pets = [pet for pet in user.pets if pet.id == value]
            if not pets:
                return {"message": f"Питомец с данным id '{value}' не найден"}, 404
            try:
                pet = pets.pop()
                pet = cls.pets_schema.load(request.json, instance=pet, session=db.session)
            except ValidationError as e:
                return {"message": str(e)}, 400
            db.session.add(pet)
            db.session.commit()
            return {"message": cls.pets_schema.dump(pet)}, 200

    @classmethod
    @check_token_and_give_admin_status_and_uuid
    def delete(cls, user_is_admin, user_uuid, value: int):
        if user_is_admin:
            # Получить питомца по id
            pet = db.session.query(PetsModel).filter_by(id=value).first()
            # Удалить питомца, если он найден
            if pet:
                db.session.delete(pet)
                db.session.commit()
                return {"message": "Deleted successfully"}, 204
            # Вернуть сообщение об ошибке и 404 код если питомец не найден
            return {"message": f"Питомец с данным id '{value}' не найден"}, 404
        return {"message": "Для удаления питомца вы должны быть администратором"}, 403
