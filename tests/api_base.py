from unittest import TestCase
import json

class TestAPIBase(TestCase):
    
    """Base test class for the auth APIs.
    Has methods for making client calls to the different auth APIs.
    
    """
    def user_get_client(self, jwt_token: str):
        return self.client.get(
            '/auth/user',
            headers=dict(
                Authorization='Bearer {}'.format(jwt_token)
            )
        )

    def logout_client(self, jwt_token: str):
        return self.client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(jwt_token)
            )
        )

    def signup_client(self, body_dict: dict):
        return self.client.post(
            '/auth/signup',
            data=json.dumps(body_dict),
            content_type='application/json'
        )

    def login_client(self, body_dict: dict):
        return self.client.post(
            '/auth/login',
            data=json.dumps(body_dict),
            content_type='application/json'
        )
