from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm, OrderForm, UpdateItemsForm, ReservationForm
from .forms import DeleteForm, DeleteUserForm, ManagerForm, ItemReportForm, EmployeeForm, DateTimeForm
from .models import db, User, Manager, Customer, Employee, Item, Order, Reservation
from .models_reports import CustomerOrders
from .auth import login_required, authorization_required
import requests
import json
import os


@app.route('/')
def home():
    """
    route handler for home 
    """
    return render_template('home.html'), 200


@app.route('/about')
def about():
    """
    route handler for the about page
    """
    return render_template('about_us.html'), 200

@app.route('/order', methods=['GET', 'POST'])
@authorization_required(roles=['customer', 'employee', 'manager'])
def order():
    """
    route handler for order
    """
    form = OrderForm()
    if form.validate_on_submit():
        item_ids = form.data['item_ids'].split(',')
        items = [Item.query.get(i) for i in item_ids]

        customer = None
        if g.user.type == 'customer':
            customer = Customer.query.get(g.user.id)
        elif form.data['customer'] != 'None':
            cust_id = form.data['customer']
            customer = Customer.query.get(cust_id)

        employee = None
        if g.user.type == 'employee':
            employee = Employee.query.get(g.user.id)
        elif form.data['employee'] != 'None':
            empl_id = form.data['employee']
            employee = Employee.query.get(empl_id)

        order = Order(
            customer=customer,
            employee=employee,
            items=items
        )
        db.session.add(order)
        db.session.commit()

    items = Item.query.all()
    return render_template(
        'order.html',
        items=items,
        form=form
    )


@app.route('/item', methods=['GET'])
@authorization_required(roles=['employee', 'manager'])
def all_items():
    """
    route handler for items to display all items in database
    """
    items = Item.query.filter_by(active=True).all()
    return render_template('items/all_items.html', items=items)


@app.route('/item/add', methods=['GET', 'POST'])
@authorization_required(roles=['employee', 'manager'])
def add_items():
    """
    route handler for add items
    """
    form = AddItemsForm()
    if form.validate_on_submit():
        item = Item(
            name=form.data['name'],
            cog=form.data['cost'],
            price=form.data['price'],
            inventory_count=form.data['count']
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.add_items'))
    items = Item.query.filter_by(active=True).all()
    return render_template('items/add_items.html', form=form, items=items)


@app.route('/item/delete', methods=['GET', 'POST'])  # this is a DELETE
@authorization_required(roles=['employee', 'manager'])
def delete_items():
    """
    route handler for delete items
    """
    form = DeleteForm()
    if form.validate_on_submit():
        name = form.data['items']
        item = Item.query.filter_by(id=name).first()
        item.active = False
        db.session.commit()
        return redirect(url_for('.all_items'))
    items = Item.query.all()
    return render_template('items/delete_items.html', form=form, items=items)


@app.route('/item/update', methods=['GET', 'POST'])  # this is a PUT
@authorization_required(roles=['employee', 'manager'])
def update_items():
    """
    route handler for update items
    """
    form = UpdateItemsForm()
    if form.validate_on_submit():
        item = Item.query.get(form.data['items'])
        item.cog = form.data['cost'],
        item.price = form.data['price'],
        item.inventory_count = form.data['count']
        db.session.commit()
        return redirect(url_for('.update_items'))
    items = Item.query.filter_by(active=True).all()
    return render_template('items/update_items.html', form=form, items=items)

@app.route('/all_users', methods=['GET', 'POST'])
@authorization_required(roles=['manager'])
def all_users():
    """
    route handler to display all users
    """
    form = DeleteUserForm()
    if form.validate_on_submit():
        id = form.data['users']
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('.all_users'))
    users = User.query.all()
    return render_template('/user/all_users.html', users=users, form=form)


@app.route('/reservation', methods=['GET', 'POST'])
@authorization_required(roles=['customer','manager', 'employee'])
def reservation():
    """
    route handler for reservations
    """
    form = ReservationForm()
    if form.validate_on_submit():
        reservation = Reservation(
            date=form.data['date'],
            time=form.data['time'],
            party=form.data['party'],
            customer=Customer.query.filter_by(id=g.user.id).first()
        )
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('.reservation'))
    if g.user.type == 'manager' or q.user.type == 'employee':
        reservations = Reservation.query.all()
    else:
        reservations = Reservation.query.filter_by(cust_id=g.user.id).all()
    return render_template('/auth/reservations.html', form=form, reservations=reservations)


@app.route('/user/manager', methods=['GET', 'POST'])
#@authorization_required(roles=['manager'])
def create_manager():
    """
    route handler to create a manager role
    """
    form = ManagerForm()
    if form.validate_on_submit():
        manager = Manager(
            name=form.data['name'],
            email=form.data['email'],
            password=form.data['password']
        )
        db.session.add(manager)
        db.session.commit()
        return redirect(url_for('.all_users'))

    return render_template('/user/create_manager.html', form=form)


@app.route('/user/employee', methods=['GET', 'POST'])
@authorization_required(roles=['manager'])
def create_employee():
    """
    route handler to create an employee role
    """
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            name=form.data['name'],
            email=form.data['email'],
            password=form.data['password'],
            pay_rate=form.data['pay_rate']
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('.all_users'))

    return render_template('/user/create_employee.html', form=form)


@app.route('/manager', methods=['GET'])
@authorization_required(roles=['employee', 'manager'])
def reports():
    """
    route handler for manager reports
    """
    return render_template('/manager/report_index.html')


@app.route('/manager/by_customer', methods=['GET', 'POST'])
@authorization_required(roles=['employee', 'manager'])
def by_customer():
    """
    route handler for tems sold by customer report
    """
    form = DeleteUserForm()
    if form.validate_on_submit():
        id = form.data['users']
        report = CustomerOrders(id)
        content = report.item_totals(id)
        users = User.query.all()

        return render_template('/manager/by_customer.html', users=users, form=form, content=content)

    users = User.query.all()
    return render_template('/manager/by_customer.html', users=users, form=form, content=None)

@app.route('/manager/by_time', methods=['GET', 'POST'])
def by_time():
    form = DateTimeForm()
    if form.validate_on_submit():
        start_date = form.data['start_date']
        end_date = form.data['end_date']
        start_time = form.data['start_time']
        end_time = form.data['end_time']
        print('valid')
        print((start_date, end_date))
        sql_start_time = (str(start_date)+' ' +str(start_time))
        sql_end_time = (str(end_date)+' ' +str(end_time))
        report = CustomerOrders(id)
        content = report.time(sql_start_time,sql_end_time)
        return render_template('/manager/by_time.html', form=form, content=content)

    return render_template('/manager/by_time.html', form=form, content=None)


@app.route('/manager/by_item', methods=['GET', 'POST'])
@authorization_required(roles=['employee', 'manager'])
def by_item():
    """
    route handler for total customer sales by item report
    """
    form = ItemReportForm()
    if form.validate_on_submit():
        id = form.data['items']
        report = CustomerOrders(id)
        content = report.customer_totals(id)
        items = Item.query.all()

        return render_template('/manager/by_item.html', items=items, form=form, content=content)

    items = Item.query.all()
    return render_template('/manager/by_item.html', items=items, form=form, content=None)

