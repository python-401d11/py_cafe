from flask_sqlalchemy import SQLAlchemy
from flask import g
from passlib.hash import sha256_crypt
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Manager(db.Model):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))
    phone = db.Column(db.String(32))


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    pay_rate = db.Column(db.Float(5, 2))


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=dt.now())
    cust_id = db.Column(db.ForeignKey('customers.id'), nullable=False)
    empl_id = db.Column(db.ForeignKey('employee.id'), nullable=False)

    # customer = db.relationship(
    #     'Customer',
    #     back_populates='customer'
    # )
    # employee = db.relationship(
    #     'Employee',
    #     back_populates='employee'
    # )
    # items = db.relationship(
    #     'Item',
    #     secondary='orders_contain',
    #     back_populates='orders'
    # )


class OrdersContain(db.Model):
    __tablename__ = 'orders_contain'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.ForeignKey('items.id'), nullable=False)

    # order = db.relationship(
    #     'Order',
    #     backref=db.backref('orders_contain', cascade='all')
    # )
    # item = db.relationship(
    #     'Order',
    #     backref=db.backref('item')
    # )


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float(10, 2))
    cog = db.Column(db.Float(10, 2))
    inventory_count = db.Column(db.Integer, default=0)

    # orders = db.relationship(
    #     'Order',
    #     secondary='orders_contain',
    #     back_populates='items'
    # )
