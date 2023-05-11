from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload, selectinload

from src import db, app
from src.models.users import UsersModel
from src.models.pets import PetsModel


def train():
    with app.app_context():
        """
        SELECT QUERIES
        """
        # SELECT * FROM clients
        query: list[UsersModel] = db.session.query(UsersModel).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # SELECT * FROM clients ORDER BY id DESC
        query: list[UsersModel] = db.session.query(UsersModel).order_by(UsersModel.id.desc()).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1)
        # ]

        # filter_by - лучше подходит для простых запросов
        # filter - лучше подходит для запросов с AND и OR
        query: UsersModel = db.session.query(UsersModel).filter_by(lastname="Ivanov").first()
        # print(query)
        # Clients(lastname=Ivanov, firstname=Ivan, id=1)
        query: UsersModel = db.session.query(UsersModel).filter(UsersModel.lastname == "Ivanov").first()
        # print(query)
        # Clients(lastname=Ivanov, firstname=Ivan, id=1)

        # Пример AND 1 вариант
        query: UsersModel = db.session.query(UsersModel).filter(
            UsersModel.lastname == "Ivanov",
            UsersModel.id >= 2).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # Пример AND 2 вариант
        query: UsersModel = db.session.query(UsersModel).filter(
            UsersModel.lastname == "Ivanov").filter(
            UsersModel.id >= 2).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # Пример AND 3 вариант
        query: UsersModel = db.session.query(UsersModel).filter(
            and_(UsersModel.lastname == "Ivanov",
                 UsersModel.id >= 2)).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # Пример LIKE
        query: UsersModel = db.session.query(UsersModel).filter(
            UsersModel.lastname.like("%Ivanov%")).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # Пример ILIKE
        query: UsersModel = db.session.query(UsersModel).filter(
            UsersModel.lastname.ilike("%ivanov%")).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3)
        # ]

        # Пример IN
        query: UsersModel = db.session.query(UsersModel).filter(
            UsersModel.id.in_([1, 2])).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2)
        # ]

        # Пример NOT IN
        query: UsersModel = db.session.query(UsersModel).filter(
            ~UsersModel.id.in_([1, 2])).all()
        # print(query)
        # [Clients(lastname=Ivanov, firstname=Ivan, id=3)]

        # Пример LIMIT 2
        query: list[UsersModel] = db.session.query(UsersModel)[:2]
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2)
        # ]

        """
        SELECT QUERIES WITH JOINS
        """
        query: list[UsersModel] = db.session.query(PetsModel).join(UsersModel.pets).all()
        # print(query)
        # [
        #   Pets(type=dog, name=Jena, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3)]),
        #   Pets(type=dog, name=Rex, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3)]),
        #   Pets(type=cat, name=Barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3)])
        # ]

        query: list[UsersModel] = db.session.query(UsersModel).join(PetsModel.clients).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[
        #       Pets(type=dog, name=Jena, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #       Pets(type=dog, name=Rex, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #       Pets(type=cat, name=Barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])])])
        # ]

        # Подсчет кол-ва строк по id
        query: int = db.session.query(func.count(UsersModel.id)).scalar()
        # print(query)
        # 5

        # Получить максимальное значение id
        query: int = db.session.query(func.max(UsersModel.id)).scalar()
        # print(query)
        # 5

        # Получить среднее арифметическое значение id
        query: int = db.session.query(func.avg(UsersModel.id)).scalar()
        # print(query)
        # 3.0

        # Получить сумму значений id
        query: int = db.session.query(func.sum(UsersModel.id)).scalar()
        # print(query)
        # 15

        query = db.session.query(UsersModel).options(joinedload(UsersModel.pets)).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3,
        #       pets=[
        #           Pets(type=dog, name=Jena, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #           Pets(type=dog, name=Rex, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #           Pets(type=cat, name=Barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])])
        #       ]
        #   ),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=4, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=5,
        #       pets=[
        #           Pets(type=cat, name=barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=5, pets=[...])])
        #       ]
        #   )
        # ]

        query = db.session.query(UsersModel).options(selectinload(UsersModel.pets)).all()
        # print(query)
        # [
        #   Clients(lastname=Ivanov, firstname=Ivan, id=1, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=2, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=3,
        #       pets=[
        #           Pets(type=dog, name=Jena, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #           Pets(type=dog, name=Rex, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])]),
        #           Pets(type=cat, name=Barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=3, pets=[...])])
        #       ]
        #   ),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=4, pets=[]),
        #   Clients(lastname=Ivanov, firstname=Ivan, id=5,
        #       pets=[
        #           Pets(type=cat, name=barsik, clients_id=[Clients(lastname=Ivanov, firstname=Ivan, id=5, pets=[...])])
        #       ]
        #   )
        # ]


if __name__ == "__main__":
    train()
