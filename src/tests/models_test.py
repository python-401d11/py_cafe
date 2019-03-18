from src.models import Manager, Customer, Employee, Order, OrderItems, Item


class TestUserModel():

    def test_create_customer(self, customer):
        assert customer

    def test_customer_data(self, customer):
        assert customer.name == 'Milo'
        assert customer.email == 'milo@test.com'
        assert customer.password == '12345'
        assert customer.role == 'customer'
        assert customer.phone == '123-456-7890'
