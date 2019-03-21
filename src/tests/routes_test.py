
class TestRoutes():

    def test_home_route(self, client):
        """
        test home route
        """
        rv = client.get('/')
        assert rv.status_code == 200
        assert b'<title>Home</title>' in rv.data

    def test_about_us_route(self, client):
        """ test about_us route """
        res = client.get('/about')
        assert res.status_code == 200
        assert b'<title>About Us</title>' in res.data
        assert b'Tim Schoen' in res.data
        assert b'Milo Anderson' in res.data
        assert b'Dan Le' in res.data

    def test_login_route(self, client):
        """
        test login route
        """
        rv = client.get('/login')
        assert rv.status_code == 200
        assert b'<title>Login</title>' in rv.data

    def test_login_post(self, client):
        """ testing login """
        res = client.post(
            '/login',
            data={
                'email': 'milo@test.com',
                'password': '12345'
            },
            follow_redirects=True
        )
        assert res.status_code == 200
        assert b'<title>Login</title>' in res.data

    def test_register_route(self, client):
        """
        test register route
        """
        rv = client.get('/register')
        assert rv.status_code == 200
        assert b'<title>Register</title>' in rv.data

    def test_reservation(self, client, auth_manager):
        """
        test reservation route
        """
        rv = client.get('/reservation')
        assert rv.status_code == 200
        assert b'<title>Make a Reservation</title>' in rv.data
      