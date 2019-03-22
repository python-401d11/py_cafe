from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, HiddenField

from wtforms.validators import DataRequired, Email, Optional
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, TimeField

from .models import Manager, Customer, Employee, Order, OrderItems, Item, User
from flask import g


class RegisterForm(FlaskForm):
    """
    Registration form
    """
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AuthForm(FlaskForm):
    """
    login authentication form
    """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class AddItemsForm(FlaskForm):
    """
    form to add items
    """
    name = StringField('name', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    cost = StringField('cost', validators=[DataRequired()])
    count = StringField('count', validators=[DataRequired()])


class DateTimeForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time')
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('Start Time')


class ReservationForm(FlaskForm):
    date = DateField('date', format='%Y-%m-%d')
    time = TimeField('time')
    party = StringField('party', validators=[DataRequired()])


class OrderForm(FlaskForm):
    """
    order form
    """
    item_ids = HiddenField('item_ids', validators=[DataRequired()], render_kw={
                           "v-model": "orderItemIds"})
    customer = SelectField('customer', validators=[Optional()], default=None)
    employee = SelectField('employee', validators=[Optional()], default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer.choices = [('None', '')] + [(str(c.id), c.name)
                                                  for c in Customer.query.all()]
        self.employee.choices = [('None', '')] + [(str(e.id), e.name)
                                                  for e in Employee.query.all()]


class UpdateItemsForm(FlaskForm):
    """
    update items form
    """
    items = SelectField('items')
    price = StringField('price', validators=[DataRequired()])
    cost = StringField('cost', validators=[DataRequired()])
    count = StringField('count', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.filter_by(active=True).all()]


class ItemReportForm(FlaskForm):
    """
    item form
    """
    items = SelectField('items')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.all()]


class DeleteForm(FlaskForm):
    """
    delete item form
    """
    items = SelectField('items')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items.choices = [(str(item.id), item.name)
                              for item in Item.query.filter_by(active=True).all()]


class DeleteUserForm(FlaskForm):
    """
    delete user form
    """
    users = SelectField('users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users.choices = [(str(user.id), user.name)
                              for user in User.query.all()]


class ManagerForm(FlaskForm):
    """
    create manager form
    """
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class EmployeeForm(FlaskForm):
    """
    employee form
    """
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    pay_rate = StringField('pay rate')


class EmployeeSelect(FlaskForm):
    """ creates a select-option element with all employees """

    employee = SelectField('employee')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee.choices = [('None', '')] + [(str(e.id), e.name)
                                                  for e in Employee.query.all()]
