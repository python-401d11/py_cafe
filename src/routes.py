from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm, OrderForm, UpdateItemsForm, DeleteForm, DeleteUserForm
from .models import db, Manager, Customer, Item, Order, User
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
@authorization_required(roles=['customer'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        item_ids = [form.data['items']]
        items = Item.query.filter(Item.id.in_(item_ids)).all()
        customer = Customer.query.filter_by(id=g.user.id).first()
        order = Order(
            customer=customer,
            items=items
        )
        db.session.add(order)
        db.session.commit()

    items = Item.query.all()
    return render_template('order.html', items=items, form=form)


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
    items= Item.query.all()
    return render_template('auth/add_items.html', form=form, items= items)


@app.route('/item/delete', methods=['GET', 'POST'])  # this is a DELETE
def delete_items():
    form = DeleteForm()
    if form.validate_on_submit():
        name = form.data['items']
        item = Item.query.filter_by(id=name).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('.delete_items'))
    items= Item.query.all()
    return render_template('auth/delete_items.html', form=form, items=items)

@app.route('/item/update', methods=['GET','POST']) # this is a PUT
def update_items():
    form = UpdateItemsForm()
    if form.validate_on_submit():
        item = Item.query.get(form.data['items'])
        item.cog=form.data['cost'],
        item.price=form.data['price'],
        item.inventory_count=form.data['count']
        # db.session.add(item)
        db.session.commit()
        return redirect(url_for('.update_items'))
    items= Item.query.all()
    return render_template('auth/update_items.html', form=form, items=items) 

@app.route('/auth/manager/all_users', methods=['GET','POST'])
def all_users():
    form = DeleteUserForm()
    if form.validate_on_submit():
        id = form.data['users']
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('.all_users'))
    users = User.query.all()
    return render_template('/auth/manager/all_users.html', users=users, form=form)

@app.route('/reservation')
def reservation():
    pass


@app.route('/employee')
def employee():
    pass
