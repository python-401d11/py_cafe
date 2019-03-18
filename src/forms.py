from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from .models import Manager, Customer, Employee, Order, OrdersContain, Item
from flask import g

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class AddItemsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    cost =  StringField('cost',validators=[DataRequired()])
    count =  StringField('count',validators=[DataRequired()])