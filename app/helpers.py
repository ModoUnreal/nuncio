"""
This code is used to store any helper functions...
"""
from flask import request, url_for
from app.models import Topic


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

def check_if_voted(post, user):
    """Checks whether a user has voted or not."""
    return any(voter.id == user.id for voter in post.voters)

def check_topic_exists(tag_name):
    """Checks whether a topic exists."""
    if Topic.query.filter_by(tag_name=tag_name).first() != None:
        return True

    return False
