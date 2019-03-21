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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = sha256_crypt.hash(password)

    @classmethod
    def check_pass_hash(cls, user, password):
        if user is not None:
            if sha256_crypt.verify(password, user.password):
                return True
        return False


class Manager(User):
    __tablename__ = 'managers'

    id = db.Column(
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    __mapper_args__ = {'polymorphic_identity': 'manager'}

    def __init__(self, name, email, password):
        User.__init__(self, name, email, password)


class Customer(User):
    __tablename__ = 'customers'

    phone = db.Column(db.String(32))
    id = db.Column(
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    orders = db.relationship('Order', back_populates='customer')
    reservations = db.relationship('Reservation', back_populates='customer')
    __mapper_args__ = {'polymorphic_identity': 'customer'}

    def __init__(self, name, email, password, phone):
        User.__init__(self, name, email, password)
        self.phone = phone


class Employee(User):
    __tablename__ = 'employees'

    pay_rate = db.Column(db.Numeric(5, 2))
    id = db.Column(
        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    orders = db.relationship('Order', back_populates='employee')
    __mapper_args__ = {'polymorphic_identity': 'employee'}

    def __init__(self, name, email, password, pay_rate):
        User.__init__(self, name, email, password)
        self.pay_rate = pay_rate


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.ForeignKey('customers.id', ondelete='CASCADE'))
    date = db.Column(db.String(32))
    time = db.Column(db.String(32))
    party = db.Column(db.String(32))

    customer = db.relationship(
        'Customer',
        back_populates='reservations'
    )


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=dt.now())
    cust_id = db.Column(db.ForeignKey('customers.id'))
    empl_id = db.Column(db.ForeignKey('employees.id'))

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

    def __init__(self, items, customer, employee):
        for item in items:
            item.inventory_count -= 1
            db.session.commit()
        self.items = items
        if customer:
            self.customer = customer
        if employee:
            self.employee = employee


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
    active = db.Column(db.Boolean, default=True)

    orders = db.relationship(
        'Order',
        secondary='order_items',
        back_populates='items'
    )

    def __repr__(self):
        return '<Item {}>'.format(self.name)
