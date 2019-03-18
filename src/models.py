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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))
    role = db.Column(db.String(16))


class Customer(User):
    __tablename__ = 'customers'

    user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(32))


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.ForeignKey('customers.id'), nullable=False)
    empl_id = db.Column(db.ForeignKey('employee.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.now())

    items = db.relationship(
        'Item',
        secondary='orders_contain',
        back_populates='orders'
    )


class OrdersContain(db.Model):
    __tablename__ = 'orders_contain'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.ForeignKey('items.id'), nullable=False)

    order = db.relationship(
        'Order',
        backref=db.backref('orders', cascade='all')
    )
    item = db.relationship(
        'Order',
        backref=db.backref('items')
    )


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float(10, 2))
    cog = db.Column(db.Float(10, 2))
    inventory_count = db.Column(db.Integer, default=0)

    orders = db.relationship(
        'Order',
        secondary='orders_contain',
        back_populates='items'
    )
