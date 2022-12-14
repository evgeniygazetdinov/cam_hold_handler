"""
class for models
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class PhotoModel(db.Model):
    """
    сохранение фото
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    store_location = db.Column(db.String())

    def __init__(self, name, store_location):
        self.name = name
        self.store_location = store_location


class EmployeeModel(db.Model):
    """
    базовый класс пример
    """

    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

    def __init__(self, employee_id, name, age, position):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position

    def __repr__(self) -> str:
        return f"{self.name}:{self.employee_id}"


class DectedPersonModel(db.Model):
    """
    персона из фото
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # store_location = db.Column(db.Integer, db.ForeignKey(PhotoModel.id))

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"


class Picture_for_store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    store_location = db.Column(db.String())
