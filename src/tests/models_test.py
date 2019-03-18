from src.models import Manager, Customer, Employee, Order, OrderItems, Item


class TestUserModels():
    """ Tests for Customer and Manager models """

    def test_create_customer(self, customer):
        assert customer

    def test_customer_data(self, customer):
        assert customer.name == 'Milo'
        assert customer.email == 'milo@test.com'
        assert customer.password == '12345'
        assert customer.phone == '123-456-7890'

    def test_create_manager(self, manager):
        assert manager

    def test_manager_data(self, manager):
        assert manager.name == 'Tim'
        assert manager.email == 'tim@test.com'
        assert manager.password == '12345'


class TestItems():
    """ Tests for Item model """

    def test_create_item(self, item):
        assert item


class TestOrders():
    """ Tests for Order model """

    def test_create_order(self, customer, employee, item, order):
        assert order
