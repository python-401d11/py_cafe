from flask import render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
import requests
import json
import os


@app.route('/')
def home():
    pass


@app.route('/customer')
def customer():
    pass


@app.route('/order')
def order():
    pass


@app.route('/item')
def item():
    pass


@app.route('/reservation')
def reservation():
    pass


@app.route('/employee')
def employee():
    pass
