from flask import Flask, Blueprint
from app.models import User, Post, Topic, Comment
from flask_restplus import API, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Nuncio Api', description='The Nuncio api.')


# Move this to app\api\models.py and make an app\api\routes.py
user_model = api.model("user", {
    "id": fields.Integer(readOnly=True, "The user's id."),
    "username": fields.String(readOnly=True, description="The user's displayed name."),
    "email": fields.String(readOnly=True, description="User's email."),
    "posts": fields.List(description="Posts made by the user."),
    "upvoted_on": fields.List(description="Name of the user."),
    "downvoted-on": fields.List(description="Name of the user."),
    }
