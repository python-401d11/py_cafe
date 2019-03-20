from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from .models import db, User, Customer, Manager, Employee, Order, OrderItems, Item


class CustomerOrders():

    def __init__(self, cust_id):
        orders = Order.query.filter_by(cust_id=cust_id).all()
        self.test = orders[0].items[0].name
