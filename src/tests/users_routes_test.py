from src.models import User, Customer, Employee, Manager


class TestUsers():

    def test_users_route_get(self, client, auth_manager):
        """ test all users route """
        rv = client.get('/all_users')
        assert rv.status_code == 200
        assert b'<title>Users</title>' in rv.data

    def test_customer_registration_get(self, auth_manager):
        """ registration page load """
        res = auth_manager.get('/register')
        assert res.status_code == 200
        assert b'<title>Register</title>' in res.data

    def test_customer_registration_post(self, auth_manager):
        """ test customer creation """
        res = auth_manager.post(
            '/register',
            data={
                'name': 'Chris',
                'phone': '1234567890',
                'email': 'chris@test.com',
                'password': '12345'
            },
            follow_redirects=True
        )
        customers = Customer.query.all()
        assert res.status_code == 200
        assert len(customers) == 1
        assert customers[0].name == 'Chris'
        assert customers[0].phone == '1234567890'
        assert customers[0].email == 'chris@test.com'
        assert customers[0].password != '12345'
