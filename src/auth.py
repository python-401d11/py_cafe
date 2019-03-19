from flask import render_template, flash, redirect, url_for, session, abort, g
from .models import db, Manager, Customer
from .forms import RegisterForm, AuthForm
from . import app
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('.login'))
        return view(**kwargs)
    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Customer.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        customer = Customer.query.filter_by(email=email).first()
        if not customer or not Customer.check_password_hash(customer, password):
            error = 'Invalid username or password'

        if not error:
            session.clear()
            session['user_id'] = customer.id
            return redirect(url_for('.home'))

        flash(error)

    return render_template('auth/login.html', form=form)
