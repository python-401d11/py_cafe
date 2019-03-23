from src.models import Order, Item


class TestOrders():

    def test_order_route_get(self, auth_customer):
        """ test order route """
        res = auth_customer.get('/order')
        assert res.status_code == 200
        assert b'<title>Order</title>' in res.data

    def test_order_route_post(self, auth_customer, items):
        """ test order creation """
        res = auth_customer.post(
            '/order',
            data={'item_ids': '1,1,2,2,2', }
        )
        orders = Order.query.all()
        assert len(orders) == 1
        assert orders[0].id == 1
        assert orders[0].cust_id == 1
        items = Item.query.all()
        assert items[0].name == 'Cheeseburger'
        assert items[0].inventory_count == 20
        assert items[1].name == 'Biscuits and Gravy'
        assert items[1].inventory_count == 9
