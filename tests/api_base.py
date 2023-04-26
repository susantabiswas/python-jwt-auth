from unittest import TestCase
import json

class TestAPIBase(TestCase):
    
    """Base test class for the auth APIs.
    Has methods for making client calls to the different auth APIs.
    
    """
    def user_get_client(self, jwt_token):
        return self.client.get(
            '/auth/user',
            headers=dict(
                Authorization='Bearer {}'.format(jwt_token)
            )
        )

    def logout_client(self, email, jwt_token):
        return self.client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(jwt_token)
            )
        )

    def signup_client(self, email, password, name):
        return self.client.post(
            '/auth/signup',
            data=json.dumps(dict(
                email=email,
                password=password,
                name=name
            )),
            content_type='application/json'
        )

    def login_client(self, email, password):
        return self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json'
        )
