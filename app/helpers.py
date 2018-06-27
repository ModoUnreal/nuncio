"""
This code is used to store any helper functions...
"""
from flask import request, url_for
from flask_login import AnonymousUserMixin
from app.models import Topic, Event


def redirect_url():
    """Function which redirects urls back a page.

       An example of usage would be when a user votes a post up or down.
       Said user would be able to vote on the index page or the item's
       specific page. So where should the user be redirected?
       
       The answer is obviously where he/she originally voted."""
    return request.args.get('next') or \
            request.referrer or \
            url_for('index')

def get_posts_from_topic(topic):
    """Gets all posts from a topic name"""
    if topic != None:
        posts = topic.posts
        return posts

    return []

def check_if_upvoted(test_post, user):
    """Checks whether a user has upvoted or not."""
    if type(user) == AnonymousUserMixin:
        return False
    else:
        return any(post.id == test_post.id for post in user.upvoted_on)

def check_if_downvoted(test_post, user):
    """Checks whether a user has downvoted or not."""
    if type(user) == AnonymousUserMixin:
        return False
    else:
        return any(post.id == test_post.id for post in user.downvoted_on)


def check_topic_exists(tag_name):
    """Checks whether a topic exists."""
    if Topic.query.filter_by(tag_name=tag_name).first() != None:
        return True

    return False

def check_event_exists(event_name):
    """Checks whether an event exists."""
    if Event.query.filter_by(event_name=event_name).first() != None:
        return True

    return False

def check_if_given_importance(test_post, user):
    """Checks whether a user has given importance to a post or not."""
    return any(post.id == test_post.id for post in user.given_importance_to)
