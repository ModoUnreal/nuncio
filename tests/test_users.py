import unittest
import sys
import os

from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Post, Topic, User


class UserTestCase(TestCase):
    def create_app(self):
        """Creates an app object for testing purposes."""
        self.app = create_app('TESTING')
        self.app_context = self.app.app_context()
        self.app_context.push()
        return self.app

    def setUp(self):
        """Sets up a test database."""
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unittest.db'
        self.app = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Removes all objects from the database and the app_context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insert_user(self):
        """Tests whether users can be inserted into the database."""
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

    def test_can_fetch_user(self):
        """Tests whether users can be fetched from the database."""
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

        self.query = User.query.filter_by(username="John").first()
        self.query = User.query.filter_by(email="example@example.com").first()
        self.query = User.query.filter_by(id=1).first()

    def test_password_is_equal(self):
        """Tests whether check_password() works."""
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.set_password("password")
        self.assertTrue(self.user.check_password('password'))

    def test_username(self):
        """Makes sure the username in the database is the same as inputted."""
        self.user = User(username="John", email="example@example.com", id=1)
        self.assertEqual("John", self.user.username)


if __name__ == '__main__':
    unittest.main(verbosity=2)


