import time
import unittest
import json
from auth.app import db
from auth.models import *
from tests.base import TestCaseBase
from tests.api_base import TestAPIBase

class TestAuthAPIs(TestCaseBase, TestAPIBase):
    def test_signup_valid_case(self):
        response = self.signup_client(email="user1@test.com", password="abc123", name="user1")

        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'User signed up successful.')
        self.assertIn('jwt_token', body)
        self.assertEqual(len(body.keys()), 3)