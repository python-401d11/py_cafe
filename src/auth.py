from flask import render_template, flash, redirect, url_for, session, abort, g
from .models import db, User, Manager, Customer, Employee
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
        g.user = User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.data['name'],
            email=form.data['email'],
            phone=form.data['phone'],
            password=form.data['password']
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('/'))
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        user = User.query.filter_by(email=email).first()
        if not user or not User.check_pass_hash(user, password):
            error = 'Invalid username or password'

        if not error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('.home'))

        flash(error)

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Thank you, bye for now')
    return redirect(url_for('.login'))
