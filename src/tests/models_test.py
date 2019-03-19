from src.models import Manager, Customer, Employee, Order, OrderItems, Item


class TestUserModels():
    """ Tests for Customer and Manager models """

    def test_create_customer(self, customer):
        assert customer

    def test_customer_data(self, customer):
        assert customer.name == 'Milo'
        assert customer.email == 'milo@test.com'
        assert customer.password
        assert customer.password != '12345'
        assert customer.phone == '123-456-7890'

    def test_create_manager(self, manager):
        assert manager

    def test_manager_data(self, manager):
        assert manager.name == 'Tim'
        assert manager.email == 'tim@test.com'
        assert manager.password
        assert manager.password != '12345'

    def test_create_employee(self, employee):
        assert employee

    def test_employee_data(self, employee):
        assert employee.name == 'Dan'
        assert employee.email == 'dan@test.com'
        assert employee.password
        assert employee.password != '54321'

    def test_user_query(self, customer, manager, employee):
        c = Customer.query.all()
        m = Manager.query.all()
        e = Employee.query.all()
        assert c[0].name == 'Milo'
        assert m[0].name == 'Tim'
        assert e[0].name == 'Dan'


class TestItems():
    """ Tests for Item model """

    def test_create_item(self, items):
        assert items

    def test_item_data(self, items):
        assert items[0].name == 'Biscuits and Gravy'
        assert items[1].price == 8.50
        assert items[0].cog == 6.54
        assert items[1].inventory_count == 22

    def test_item_query(self, items):
        i = Item.query.all()
        assert i[0].name == 'Biscuits and Gravy'


class TestOrders():
    """ Tests for Order model """

    def test_create_order(self, customer, employee, items, order):
        assert order

    def test_order_data(self, customer, employee, items, order):
        assert order.customer.name == 'Milo'
        assert order.employee.name == 'Dan'
        assert order.items[0].name == 'Biscuits and Gravy'
        assert order.items[1].name == 'Cheeseburger'
