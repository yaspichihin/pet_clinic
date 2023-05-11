# Укажем различные системные конфигурации Базы Данных

from pathlib import Path


BASE_DIR = Path(__file__).parent


class Config:
    # SQLALCHEMY_DATABASE_URI - местоположение DB
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "data" / "db.sqlite3")
    # SQLALCHEMY_TRACK_MODIFICATIONS - Отключить отслеживание изменения объектов и посылку сигналов
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ключ и алгоритм для JWT токена
    JWT_KEY = "51ad97saf2aws54asd6afs8a6"
    JWT_ALGORITHMS = "HS256"
