from flask_sqlalchemy import SQLAlchemy
from flask import g
from passlib.hash import sha256_crypt
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'


class Customer(User):
    __tablename__ = 'customers'


class Employee(db.Model):
    __tablename__ = 'employee'


class Order(db.Model):
    __tablename__ = 'orders'


class OrdersContain(db.Model):
    __tablename__ = 'orders_contain'


class Item(db.Model):
    __tablename__ = 'items'

