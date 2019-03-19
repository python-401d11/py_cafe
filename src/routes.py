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

@app.route('/item/delete', methods=['POST']) # this is a DELETE
def delete_items():
    form = DeleteForm()
    pass

@app.route('/item/update', methods=['POST']) # this is a PUT
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
        return redirect(url_for('/')) 


@app.route('/reservation')
def reservation():
    pass


@app.route('/employee')
def employee():
    pass
