from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from .models import Manager, Customer, Employee, Order, OrderItems, Item
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

class OrderForm(FlaskForm):
    items = SelectField('items')
    number_ordered = StringField('number_ordered', validators=[DataRequired()])
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.items.choices = [(item.id,item.name)for item in Item.query.all()]
    