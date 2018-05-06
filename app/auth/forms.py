from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from ..models import User


class LoginForm(FlaskForm):
    """Form for a user to login.
    
    Parameters
    ----------
    username : str
        Contains the username as a string.
    password : str
        The actual password the user enters, so no hashing involved.
    remember_me : boolean
        Sets remember_me to 'True' or 'False'."""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Form for registering a new user.
    
    Parameters
    ----------
    username : str
        Contains the new username that will be entered into the database.
    email : str
        Contains the email as a string.
    password : str
        This is the password that will be set to the new profile, no hashing."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Used to validate a username, so that the username is unique."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Makes sure that the email is a proper email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
