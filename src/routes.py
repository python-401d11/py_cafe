from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm, OrderForm, UpdateItemsForm, DeleteForm
from .models import db, Manager, Customer, Item, Order
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.add_template_global
def get_items():
    return Items.query.all()


@app.route('/customer')
def customer():
    pass


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        items_list = [form.data['items']]
        order = Order(
            items=items_list
        )
        db.session.add(order)
        dp.session.commit()

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
        return redirect(url_for('/'))

    return render_template('auth/add_items.html', form=form)

@app.route('/item/delete', methods=['GET','POST']) # this is a DELETE
def delete_items():
    form = DeleteForm()
    if form.validate_on_submit():
        name = form.data['items']
        item = Item.query.filter_by(id=name).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('/'))
    items= Item.query.all()
    return render_template('auth/delete_items.html', form=form, items=items)

@app.route('/item/update', methods=['GET','POST']) # this is a PUT
def update_items():
    form = UpdateItemsForm()
    if form.validate_on_submit():
        item = Item(
            name = form.data['name'],
            cog = form.data['cost'],
            price = form.data['price'],
            inventory_count = form.data['count']
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('auth/update_items.html')) 


@app.route('/reservation')
def reservation():
    pass


@app.route('/employee')
def employee():
    pass
