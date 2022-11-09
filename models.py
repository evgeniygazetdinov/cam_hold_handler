"""
class for models
"""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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


class PhotoModel(db.Model):
    """
    персона из фото
    """

    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    place_for_store = db.Column(db.String())
    date = db.Column(db.Datetime(), default=datetime.datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"


class DectedPersonModel(db.Model):
    """
    персона из фото
    """

    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    photo_where_located = db.Column(db.Integer, db.ForeignKey(PhotoModel.id))

    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"
