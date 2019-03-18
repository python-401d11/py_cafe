from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm
from .models import db, Manager, Customer
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.data['name'],
            email=form.data['email'],
            phone=form.data['phone']
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('/'))
    return render_template('auth/register.html', form=form)


@app.route('/customer')
def customer():
    pass


@app.route('/order')
def order():
    pass


@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    form = AddItemsForm()
    return render_template('auth/add_items.html', form=form)


@app.route('/reservation')
def reservation():
    pass


@app.route('/employee')
def employee():
    pass
