
class TestClass():

    def test_home_route(self, client):
        """
        test home route
        """
        rv = client.get('/')
        assert rv.status_code == 200
        assert b'<title>Home</title>' in rv.data

    def test_login_route(self, client):
        """
        test login route
        """
        rv = client.get('/login')
        assert rv.status_code == 200
        assert b'<title>Login</title>' in rv.data

    def test_register_route(self, client):
        """
        test register route
        """
        rv = client.get('/register')
        assert rv.status_code == 200
        assert b'<title>Register</title>' in rv.data

    def test_users_route(self, client, auth_manager):
        """
        test all users route
        """
        rv = client.get('/all_users')
        assert rv.status_code == 200
        assert b'<title>Users</title>' in rv.data
