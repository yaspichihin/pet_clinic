from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config


# Создадим экземпляр приложения Flask
app = Flask(__name__)

# Передача настроек в приложение Flask
app.config.from_object(Config)

# db - представляет объект Базы Данных
db = SQLAlchemy(app)

# Импорт моделей после определения db
from src.models.pets import PetsModel
from src.models.users import UsersModel
from src.models.tables import clients_pets

# migrate - представляет объект миграции
migrate = Migrate(app, db)

# Создаем экземпляр класса Api для указания, что
# хотим использовать flask_restful
api = Api(app)

# Импорт маршрутизаторов, самое главное делать импорт после определения db
from src.routers.pets import PetsApi
from src.routers.users import UsersApi, BindApi
from src.routers.auth import AuthRegisterApi, AuthLoginApi, AuthLogoutApi

# Добавление маршрутизаторов к api
api.add_resource(AuthRegisterApi, "/register", strict_slashes=False)
api.add_resource(AuthLoginApi, "/login", strict_slashes=False)
api.add_resource(AuthLogoutApi, "/logout", strict_slashes=False)

api.add_resource(PetsApi, "/pets", "/pets/<int:value>", "/pets/<string:value>", strict_slashes=False)
api.add_resource(BindApi, "/users/bind", strict_slashes=False)
api.add_resource(UsersApi, "/users", "/users/<int:value>", "/users/<string:value>", strict_slashes=False)


SWAGGER_URL = ""
API_URL = "/static/swagger.yaml"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Flask tutorial"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
