import unittest
import sys
import os
from datetime import datetime

from flask_testing import TestCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Post, Topic, Event, Comment
from app.helpers import check_event_exists, check_topic_exists


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

    def test_submit_basic(self):
        """Tests whether posts can be put inside the database."""
        self.post = Post(title="Title", text="Text", user_id=1,
                    topics=[Topic(tag_name="topic1"),
                    Topic(tag_name="topic2")], event=Event(event_name="Test"))
        self.post.upvotes = 1
        self.post.downvotes = 0
        self.post.importance = 1
        self.post.score = self.post.get_score()
        db.session.add(self.post)
        db.session.commit()

    def test_check_event_exists_func(self):
        """Tests whether check_event_exists function work."""
        self.test_event_str = "test"
        self.test_event = Event(event_name=self.test_event_str)
        db.session.add(self.test_event)
        db.session.commit()

        self.assertTrue(check_event_exists(self.test_event_str))

        self.assertFalse(check_event_exists("BEFALSE"))

    def test_check_topic_exists_func(self):
        """Tests whether check_topic_exists function work."""
        self.test_topic_str = "test"
        self.test_topic = Topic(tag_name=self.test_topic_str)
        db.session.add(self.test_topic)
        db.session.commit()

        self.assertTrue(check_topic_exists(self.test_topic_str))

        self.assertFalse(check_topic_exists("BEFALSE"))

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

    def test_can_delete_post(self):
        """Tests whether a post can be deleted."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=99)
        db.session.add(self.post)
        db.session.commit()

        db.session.delete(self.post)
        db.session.commit()

        posts = self.assertIsNone(Post.query.filter_by(id=99).first())

    def test_upvoting(self):
        """Tests whether posts can be upvoted or not."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        self.post.upvotes = 1
        db.session.add(self.post)
        db.session.commit()

        self.post.upvotes += 1
        db.session.commit()

    def test_downvoting(self):
        """Tests whether posts can be downvoted or not."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        self.post.downvotes = 1
        db.session.add(self.post)
        db.session.commit()
 
        self.post.downvotes += 1
        db.session.commit()

    def test_add_new_comment(self):
        """Tests whether a new comment can be added."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        db.session.add(self.post)
        db.session.commit()

        self.comment = Comment(text="This is a test", post_id=self.post.id)
        db.session.add(self.comment)
        db.session.commit()

    def test_filter_comment(self):
        """Tests whether a comment can be filtered 
           by post_id."""
        self.post = Post(title="Title", text="Text", user_id=1, topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        db.session.add(self.post)
        db.session.commit()

        self.comment = Comment(text="This is a test", post_id=self.post.id)
        db.session.add(self.comment)
        db.session.commit()

        comments = Comment.query.filter_by(post_id=self.post.id)
        for i in comments:
            self.assertEqual(i.text, self.comment.text)

    def test_time_type_setting(self):
        """Tests whether the time type can be set correctly."""
        self.post = Post(title="Title", text="Text", user_id=1,
                topics=[Topic(tag_name="topic1"), Topic(tag_name="topic2")], id=1)
        # Difference between the two timestamps is in minutes.
        # So timetype should equal 0.
        self.post.timestamp = datetime(2018, 6, 29, 10, 00, 00)
        self.test_timestamp = datetime(2018, 6, 29, 10, 2, 00)
        self.post.get_minutes(input_time=self.test_timestamp)
        self.assertEqual(0, self.post.time_type)
        self.assertFalse(1 == self.post.time_type)

        # Difference between the two timestamps is in hours.
        # So timetype should equal 1.
        self.post.timestamp = datetime(2018, 6, 29, 10, 00, 00)
        self.test_timestamp = datetime(2018, 6, 29, 11, 2, 00)
        self.post.get_minutes(input_time=self.test_timestamp)
        self.assertEqual(1, self.post.time_type)
        self.assertFalse(2 == self.post.time_type)

        # Difference between the two timestamps is in hours.
        # So timetype should equal 1.
        self.post.timestamp = datetime(2018, 6, 29, 10, 00, 00)
        self.test_timestamp = datetime(2018, 6, 30, 11, 2, 00)
        self.post.get_minutes(input_time=self.test_timestamp)
        self.assertEqual(2, self.post.time_type)
        self.assertFalse(1 == self.post.time_type)
