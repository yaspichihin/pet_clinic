from src import db


clients_pets = db.Table(
    "clients_pets",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("pet_id", db.Integer, db.ForeignKey("pets.id"), primary_key=True),
)
