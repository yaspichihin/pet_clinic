from datetime import date

from src import app, db
from src.models.pets import PetsModel
from src.models.users import UsersModel


def insert_data():

    # Тестовые данные Pets
    sima = PetsModel(animal_type="cat", name="Sima", birthdate=date(2020, 2, 13),
                     sex="male", breed="mongrel")

    marsik = PetsModel(animal_type="cat", name="Marsik", birthdate=date(2019, 2, 13),
                       sex="male", breed="mongrel")

    jena = PetsModel(animal_type="dog", name="Jena", birthdate=date(2016, 11, 1),
                     sex="female", breed="husky")

    rex1 = PetsModel(animal_type="dog", name="Rex", birthdate=date(2016, 5, 1),
                     sex="male", breed="shepherd")

    rex2 = PetsModel(animal_type="dog", name="Rex", birthdate=date(2014, 9, 17),
                     sex="male", breed="husky")

    barsik1 = PetsModel(animal_type="cat", name="Barsik", birthdate=date(2014, 3, 23),
                        sex="male", breed="mongrel")

    barsik2 = PetsModel(animal_type="cat", name="Barsik", birthdate=date(2018, 3, 15),
                        sex="male", breed="mongrel")

    barsik3 = PetsModel(animal_type="cat", name="Barsik", birthdate=date(2012, 6, 20),
                        sex="male", breed="mongrel")

    # Тестовые данные Users
    ivanov = UsersModel(email="ivanov@mail.com", password="password1",
                        firstname="Ivan", lastname="Ivanov", phone=81231231212,
                        sex="male", birthdate=date(2000, 3, 21))

    petrov = UsersModel(email="petrov@mail.com", password="password2",
                        firstname="Petr", lastname="Petrov", phone=81231231211,
                        sex="male", birthdate=date(1998, 3, 21))

    maksimov = UsersModel(email="maksimov@mail.com", password="password3",
                          firstname="Maksim", lastname="Maksimov", phone=81231231213,
                          sex="male", birthdate=date(1991, 3, 21), is_admin=True)

    # Закрепляем животных за пользователями
    ivanov.pets = [jena, rex1, barsik1]
    petrov.pets = [rex2, barsik2]
    maksimov.pets = [barsik3]

    # Незакрепленные животные
    # sima, marsik

    db.session.add(sima)
    db.session.add(marsik)
    db.session.add(jena)
    db.session.add(rex1)
    db.session.add(rex2)
    db.session.add(barsik1)
    db.session.add(barsik2)
    db.session.add(barsik3)

    db.session.add(ivanov)
    db.session.add(petrov)
    db.session.add(maksimov)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    with app.app_context():
        insert_data()
    print('Successfully populated!')
