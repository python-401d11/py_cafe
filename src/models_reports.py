from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from .models import db, User, Customer, Manager, Employee, Order, OrderItems, Item


class CustomerOrders():

    def __init__(self, cust_id):
        self.cust_id = cust_id

    def item_totals(self, cust_id):
        rtn = []
        order_ids = []
        counts = []
        order_items_list = []

        orders = Order.query.filter_by(cust_id=cust_id).all()
        for order in orders:
            order_ids.append(order.id)
        for i in order_ids:
            orderd_items = OrderItems.query.filter_by(order_id=i).all()
            for j in orderd_items:
                order_items_list.append(j.item_id)
        items = Item.query.all()
        for item in items:
            counts.append((item.name, order_items_list.count(item.id)))
        return counts

    def customer_totals(self, item_id=0):
        rtn = []
        SQL = """ 
        select users.name, count(items.id), items.name from users
inner join customers on users.id = customers.id
inner join orders on customers.id=orders.cust_id 
inner join order_items on orders.id=order_items.order_id 
inner join items on order_items.item_id=items.id
where items.id={}
group by users.name, items.name; """.format(item_id)
        test = db.session.execute(SQL)
        for row in test:
            rtn.append(row)
        return rtn
    
    def time(self,start_time, end_time):
        rtn =[]
        SQL = """select users.name, orders.date_created, count(items.id), items.name from users
inner join customers on users.id = customers.id
inner join orders on customers.id=orders.cust_id 
inner join order_items on orders.id=order_items.order_id 
inner join items on order_items.item_id=items.id
where items.name='cheeseburger'
and orders.date_created > '{}' 
and orders.date_created < '{}' 
group by users.name, orders.date_created, items.name;""".format(start_time,end_time)
        test = db.session.execute(SQL)
        for row in test:
            rtn.append(row)
        return rtn
