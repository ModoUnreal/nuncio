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

    def test_register_user(self):
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

    def test_voting(self):
        """Tests whether a user can up or downvote."""
        self.post = Post(title="Title", text="Text")
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.upvoted_on.append(self.post)

        self.post = Post(title="Rick", text="Jaime")
        self.user.downvoted_on.append(self.post)
        for i in self.user.upvoted_on:
            self.assertEqual(i.title, "Title")

        for i in self.user.downvoted_on:
            self.assertEqual(i.title, "Rick")

    def test_giving_importance(self):
        """Tests whether a user can give importance."""
        self.post = Post(title="Title", text="Text")
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.given_importance_to.append(self.post)

        for i in self.user.given_importance_to:
            self.assertEqual(i.title, "Title")

    def test_sum_post_scores(self):
        """Tests to see whether the program can iterate through a users
           post's score."""
        self.user = User(username="John", email="example@example.com", id=1)
        self.user.importance_debt = 0
        db.session.add(self.user)
        db.session.commit()
        self.post = Post(title="Title", text="Text", user_id=self.user.id)
        self.post.upvotes = 1
        self.post.downvotes = 0
        self.post.score = self.post.get_score()
        db.session.add(self.post)
        db.session.commit()

        self.assertEqual(self.user.sum_post_scores(), 1)
