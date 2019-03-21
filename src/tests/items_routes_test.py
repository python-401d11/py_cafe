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
            data={
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
        """ test delete item route """
        rv = client.get('/item/delete')
        assert rv.status_code == 200
        assert b'<title>Delete Items</title>' in rv.data

    def test_item_delete_post(self, auth_manager, items):
        """ testing item deletion """
        res = auth_manager.post(
            '/item/delete',
            data={'items': 1},
            follow_redirects=True
        )
        items = Item.query.all()
        assert len(items) == 2
        assert items[0].active is True
        assert items[1].active is False

    def test_item_update_get(self, auth_manager, items):
        """ test item update route """
        res = auth_manager.get('/item/update')
        assert res.status_code == 200
        assert b'<title>Update Items</title>' in res.data
    
    def test_item_update_post(self, auth_manager, items):
        """ test item updating """
        res = auth_manager.post(
            '/item/update',
            data={
                'items': 1,
                'cost': 0.50,
                'price': 20.00,
                'count': 42
            },
            follow_redirects=True
        )
        saved_items = Item.query.all()
        assert len(saved_items) == 2
        assert saved_items[1].cog == 0.50
        assert saved_items[0].cog != 0.50
        assert saved_items[1].price == 20.00
        assert saved_items[0].price != 20.00
        assert saved_items[1].inventory_count == 42
        assert saved_items[0].inventory_count != 42
