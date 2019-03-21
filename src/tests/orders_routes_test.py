from src.models import Manager, Customer, Employee, Order, OrderItems, Item


class TestOrders():

    def test_order_route_get(self, auth_customer):
        """ test order route """
        res = auth_customer.get('/order')
        assert res.status_code == 200
        assert b'<title>Order</title>' in res.data

    def test_order_route_post(self, auth_customer):
        """ test order creation """
        res = auth_customer.post(
            '/order',
            data={'item_ids': '1,1,2,2,2', }
        )
        orders = Order.query.all()
        assert orders[0].id == 1
