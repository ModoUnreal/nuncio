import unittest
import sys
import os

from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Post, Topic
from app.routes import submit


class PostTestCase(TestCase):
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

    def test_submit(self):
        """Tests whether posts can be put inside the database."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")])
        self.post.upvotes = 1
        self.post.downvotes = 0
        self.post.importance = 1
        self.post.score = self.post.get_score()
        db.session.add(self.post)
        db.session.commit()

    def test_can_fetch_post(self):
        """Tests whether posts can be fetched from the database."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        self.post.upvotes = 1
        self.post.downvotes = 0
        self.post.importance = 1
        self.post.score = self.post.get_score()
        db.session.add(self.post)
        db.session.commit()

        self.query = Post.query.filter_by(id=1).first()
        self.query = Post.query.filter_by(user_id=1).first()


if __name__ == '__main__':
    unittest.main(verbosity=2)
