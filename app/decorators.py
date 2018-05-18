from flask import request, url_for
from flask_login import current_user
from functools import wraps
from app.models import User, Post, Topic
from app import db


def update_user(func):
    """Function used to update a user every time the user visits a new
       page."""
    @wraps(func)
    def update_user_decorator(*args, **kwargs):
        current_user.score = current_user.sum_post_scores()
        db.session.commit()
        return func(*args, **kwargs)

    return update_user_decorator
