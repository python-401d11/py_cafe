from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
from .forms import RegisterForm, AddItemsForm
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
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
