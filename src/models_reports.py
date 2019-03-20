from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from .models import db, User, Customer, Manager, Employee, Order, OrderItems, Item


class CustomerOrders():

    def __init__(self, cust_id):
        self.cust_id= cust_id

       
        
    def item_totals(self, cust_id):
        rtn= []
        order_ids =[]
        counts = []
        order_items_list =[]
       
        orders = Order.query.filter_by(cust_id=cust_id).all()
        for order in orders:
            order_ids.append(order.id)
        for i in order_ids:
            orderd_items = OrderItems.query.filter_by(order_id= i).all()
            for j in orderd_items:
                order_items_list.append(j.item_id)
        items = Item.query.all()
        for item in items:
            counts.append((item.name,order_items_list.count(item.id)))
        return counts
