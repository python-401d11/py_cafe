from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, HiddenField
from wtforms.validators import DataRequired
from .models import Manager, Customer, Employee, Order, OrderItems, Item, User
from flask import g


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AuthForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AddItemsForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    cost = StringField('cost', validators=[DataRequired()])
    count = StringField('count', validators=[DataRequired()])


class OrderForm(FlaskForm):
    item_ids = HiddenField('item_ids', validators=[DataRequired()], render_kw={
                           "v-model": "orderItemIds"})


class UpdateItemsForm(FlaskForm):
    items = SelectField('items')
    price = StringField('price', validators=[DataRequired()])
    cost = StringField('cost', validators=[DataRequired()])
    count = StringField('count', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.all()]
class ItemForm(FlaskForm):
    items = SelectField('items')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.all()]
    

class DeleteForm(FlaskForm):
    items = SelectField('items')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.all()]

        
class DeleteUserForm(FlaskForm):
    users = SelectField('users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users.choices = [(str(user.id), user.name)
                              for user in User.query.all()]


class ManagerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
