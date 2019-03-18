from src.models import db as _db
from src.models import Manager, Customer, Employee, Order, OrdersContain, Item
from src import app as _app
import pytest
import os


@pytest.fixture()
def app(request):
    """ Session-wide testable Flask app """
    _app.config.from_mapping(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False
    )
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):
    """ Session-wide test DB """

    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()
    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    """ Create new DB session for testing """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()
    request.addfinalizer(teardown)

    return session


@pytest.fixture()
def client(app, db, session):
    """ Create test client """
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def customer(session):
    """ Create test user with customer role """
    user = User(
        name='Milo',
        email='milo@test.com',
        password='12345',
        role='customer'
    )
    customer = Customer(
        phone='123-456-7890',
        user=user
    )
    session.add(customer)
    session.commit()
    return customer


@pytest.fixture()
def manager(session):
    """ Create test user with manager role """
    user = User(
        name='Tim',
        email='tim@test.com',
        password='12345',
        role='manager'
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture()
def employee(session):
    """ Create test employee """
    employee = Employee(
        name='Dan',
        pay_rate=10.50
    )


@pytest.fixure()
def item(session):
    """ Create test item """
    item = Item(
        name='Biscuits and Gravy',
        price=9.50,
        cog=6.54,
        inventory_count=12
    )
    session.add(item)
    session.commit()
    return item


@pytest.fixture()
def order(session, customer, employee, item):
    """ Create test order """
    order = Order(
        customer=customer,
        employee=employee,
        item=item
    )
    session.add(order)
    session.commit()
    return order
