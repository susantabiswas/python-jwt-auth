import unittest
from flask_testing import TestCase
from auth.app import app

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("auth.config.TestConfig")
        return app
        

    def test_test_configuration(self):
        self.assertTrue(app.config['ENV'] == 'testing')
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == "mysql://root:root@127.0.0.1:3306/flask_jwt_test")
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertTrue(app.config['TESTING'] == True)

        
        self.assertTrue(app.config['JWT_SECONDS'] == 2)
        self.assertTrue(app.config['JWT_MINUTES'] == 0)
        self.assertTrue(app.config['JWT_DAYS'] == 0)

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("auth.config.DevConfig")
        return app

    def test_dev_configuration(self):
        self.assertTrue(app.config['ENV'] == 'development')
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == "mysql://root:root@127.0.0.1:3306/flask_jwt")
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertTrue(app.config['TESTING'] == True)

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("auth.config.ProdConfig")
        return app

    def test_production_configuration(self):
        self.assertTrue(app.config['ENV'] == 'production')
        self.assertFalse(app.config['SQLALCHEMY_DATABASE_URI'] == "mysql://root:root@127.0.0.1:3306/flask_jwt_test")
        self.assertTrue(app.config['DEBUG'] == False)
        self.assertTrue(app.config['TESTING'] == False)

if __name__ == "__main__":
    unittest.main()