from functools import wraps

import jwt
from flask import request

from src import app, db
from src.models.users import UsersModel


# TODO: в целях безопасности возможно потребуется поменять messages
# Декоратор для проверки регистрации пользователя при обращении к endpoint
def check_token_and_give_admin_status_and_uuid(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):

        # Получаем access_token из cookies
        token = request.cookies.get('access_token')
        # Если X-API-KEY определен, то используем его, вместо cookies
        if request.headers.get('X-API-KEY', ''):
            token = request.headers.get('X-API-KEY', '')

        if not token:
            return {"message": "Требуется пройти аутентификацию токен не определен"}, 401

        # Попытка декодировать токен и получить uuid пользователя
        try:
            user_data = jwt.decode(
                token,
                app.config['JWT_KEY'],
                app.config['JWT_ALGORITHMS']
            )
            uuid = user_data['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return {"message": "Токен не содержал поле 'user_id' или просрочен"}, 401

        # Получения пользователя по uuid
        user = db.session.query(UsersModel).filter_by(uuid=uuid).first()
        if not user:
            return {"message": "Данный пользователь по UUID не найден, проверьте токен"}, 401

        # Дополнительно пробросим являться ли пользователь
        # администратором или нет и его uuid
        kwargs.update(
            {
                "user_is_admin": user.is_admin,
                "user_uuid":  user.uuid
            }
        )
        return func(self, *args, **kwargs)

    return wrapper
