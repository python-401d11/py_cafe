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
    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Manager(User):
    __tablename__ = 'managers'

    id = db.Column(db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }


class Customer(User):
    __tablename__ = 'customers'

    id = db.Column(db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(32))

    orders = db.relationship(
        'Order',
        back_populates='customer'
    )
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    pay_rate = db.Column(db.Numeric(5, 2))

    orders = db.relationship(
        'Order',
        back_populates='employee'
    )


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=dt.now())
    cust_id = db.Column(db.ForeignKey('customers.id'), nullable=False)
    empl_id = db.Column(db.ForeignKey('employees.id'), nullable=False)

    customer = db.relationship(
        'Customer',
        back_populates='orders'
    )
    employee = db.relationship(
        'Employee',
        back_populates='orders'
    )
    items = db.relationship(
        'Item',
        secondary='order_items',
        back_populates='orders'
    )


class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.ForeignKey('items.id'), nullable=False)

    order = db.relationship(
        'Order',
        backref=db.backref('order_items', cascade='all')
    )
    item = db.relationship(
        'Item',
        backref=db.backref('order_items')
    )


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    cog = db.Column(db.Numeric(10, 2))
    inventory_count = db.Column(db.Integer, default=0)

    orders = db.relationship(
        'Order',
        secondary='order_items',
        back_populates='items'
    )

    def __repr__(self):
        return '<Item {}>'.format(self.name)
