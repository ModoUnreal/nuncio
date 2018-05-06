"""
This code is used to store any helper functions...
"""
from flask import request, url_for


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
    for voter in post.voters:
        if voter.id == user.id:
            return True
        elif voter.id != user.id:
            return False
