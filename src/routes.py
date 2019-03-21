from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm, OrderForm, UpdateItemsForm, ReservationForm
from .forms import DeleteForm, DeleteUserForm, ManagerForm, ItemForm, EmployeeForm
from .models import db, User, Manager, Customer, Employee, Item, Order, Reservation
from .models_reports import CustomerOrders
from .auth import login_required, authorization_required
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/about')
def about():
    return render_template('about_us.html'), 200


@app.add_template_global
def get_items():
    return Items.query.all()


@app.route('/customer')
def customer():
    pass


@app.route('/order', methods=['GET', 'POST'])
@authorization_required(roles=['customer', 'employee', 'manager'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        item_ids = form.data['item_ids'].split(',')
        items = [Item.query.get(i) for i in item_ids]

        if g.user.type == 'customer':
            customer = Customer.query.get(g.user.id)
        elif form.data['customer']:
            cust_id = form.data['customer']
            customer = Customer.query.get(cust_id)

        if g.user.type == 'employee':
            employee = Employee.query.get(g.user.id)
        elif form.data['employee']:
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
# @authorization_required(roles=['employee', 'manager'])
def all_items():
    items = Item.query.filter_by(active=True).all()
    return render_template('items/all_items.html', items=items)


@app.route('/item/add', methods=['GET', 'POST'])
def add_items():
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
def delete_items():
    form = DeleteForm()
    if form.validate_on_submit():
        name = form.data['items']
        item = Item.query.filter_by(id=name).first()
        item.active = False
        db.session.commit()
        return redirect(url_for('.delete_items'))
    items = Item.query.all()
    return render_template('items/delete_items.html', form=form, items=items)


@app.route('/item/update', methods=['GET', 'POST'])  # this is a PUT
def update_items():
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
def all_users():
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
@authorization_required(roles=['customer'])
def reservation():
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
    reservations = Reservation.query.filter_by(id=g.user.id)
    return render_template('/auth/reservations.html', form=form, reservations=reservations)


@app.route('/user/manager', methods=['GET', 'POST'])
def create_manager():
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
def create_employee():
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
def reports():
    return render_template('/manager/report_index.html')


@app.route('/manager/by_customer', methods=['GET', 'POST'])
def by_customer():
    form = DeleteUserForm()
    if form.validate_on_submit():
        id = form.data['users']
        report = CustomerOrders(id)
        content = report.item_totals(id)
        users = User.query.all()

        return render_template('/manager/by_customer.html', users=users, form=form, content=content)

    users = User.query.all()
    return render_template('/manager/by_customer.html', users=users, form=form, content=None)


@app.route('/manager/by_item', methods=['GET', 'POST'])
def by_item():
    form = ItemForm()
    if form.validate_on_submit():
        id = form.data['items']
        report = CustomerOrders(id)
        content = report.customer_totals(id)
        items = Item.query.all()

        return render_template('/manager/by_item.html', items=items, form=form, content=content)

    items = Item.query.all()
    return render_template('/manager/by_item.html', items=items, form=form, content=None)

