from flask import Flask
from app.models import User, Post, Topic, Comment
from flask_restplus import Resource, fields, ModelSchema, Namespace


# Move this to app\api\models.py and make an app\api\routes.py
user_model = api.model("user", {
    "id": fields.Integer(readOnly=True, "The user's id."),
    "username": fields.String(readOnly=True, description="The user's displayed name."),
    "email": fields.String(readOnly=True, description="User's email."),
    "posts": fields.List(description="Posts made by the user."),
    "upvoted_on": fields.List(description="Name of the user."),
    "downvoted-on": fields.List(description="Name of the user."),
    })

class UserSchema(ModelSchema):
    class Meta:
        model = User

users_api = Namespace('users')
api.add_namespace(users_api)

@users_api.route('/')
class UsersList(Resource):

    @users_api.response(UserSchema(many=True))
    def get(self):
        return User.query.all()

@users_api.route('/<int:user_id>')
@users_api.resolve_object('user', lambda kwargs: User.query.get_or_404(kwargs.pop('user.id')))
class UserById(Resource): 
    @users_api.response(UserSchema())
    def get(self, user):
        return user
