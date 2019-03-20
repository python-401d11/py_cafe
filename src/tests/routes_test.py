
class TestClass():
    @classmethod
    def setup_class(cls):
        print('setup_class')
    @classmethod
    def teardown_class(cls):
        pass

    def test_home_route(self, client):
        """
        test home route
        """
        rv = client.get('/')
        assert rv.status_code == 200
        assert b'<h1>Home Page</h1>' in rv.data   

    def test_login_route(self, client):
        """
        test login route
        """
        rv = client.get('/login')
        assert rv.status_code == 200
        assert b'<h2>Login:</h2>' in rv.data            

    def test_register_route(self,client):
        """
        test register route
        """
        rv = client.get('/register')
        assert rv.status_code == 200
        assert b'<h2>Register:</h2>' in rv.data 

    def test_order_route(self,client, customer):
        """
        test order route
        """
        rv = client.post(
            '/order',
            data = {'email':customer.email, 'password':customer.password},
            follow_redirects = True,
        )
        assert rv.status_code == 200

    def test_add_route(self,client):
        """
        test add item route
        """
        rv = client.get('/item/add')
        assert rv.status_code == 200
        assert b'<h2>Add Item:</h2>' in rv.data 

    def test_delete_route(self,client):
        """
        test add item route
        """
        rv = client.get('/item/delete')
        assert rv.status_code == 200
        assert b'<h2>Delete Item:</h2>' in rv.data    

    def test_users_route(self,client,manager):
        """
        test all users route
        """
        rv = client.get('/auth/manager/all_users')
        assert rv.status_code == 200
        assert b'<th>Name</th>' in rv.data    