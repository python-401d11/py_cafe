from src.models import Order, Item


class TestItems():

    def test_item_all_get(self, auth_manager, items):
        """ all_items landing page """
        res = auth_manager.get('/item')
        assert res.status_code == 200
        assert b'<title>All Items</title>' in res.data
        assert b'Cheeseburger' in res.data
        assert b'Biscuits and Gravy' in res.data

    def test_item_add_get(self, client, auth_manager):
        """
        test add item route
        """
        rv = client.get('/item/add')
        assert rv.status_code == 200
        assert b'<title>Add Items</title>' in rv.data

    def test_item_add_post(self, auth_manager):
        """ testing item creation """
        res = auth_manager.post(
            '/item/add',
            data = {
                'name': 'BLT',
                'cost': 4.50,
                'price': 7.95,
                'count': 12
            }
        )
        items = Item.query.all()
        assert len(items) == 1
        assert items[0].name == 'BLT'
        assert items[0].cog == 4.5

    def test_item_delete_get(self, client, auth_manager):
        """
        test add item route
        """
        rv = client.get('/item/delete')
        assert rv.status_code == 200
        assert b'<title>Delete Items</title>' in rv.data