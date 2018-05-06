from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class SubmitForm(FlaskForm):
    """Form for submitting posts.
    
    
    Parameters
    ----------
    title : str
        Contains the title of the post.
    topics : list
        Contains a list of all the topics.
    text : str
        The base text of the post, if needed."""
    
    title = StringField('Title', validators=[DataRequired()])
    topics = StringField('Topics', validators=[DataRequired()])
    text = StringField('Link', validators=[Length(min=0, max=140)])
    submit = SubmitField('Send')

class CommentForm(FlaskForm):
    """Form for making a comment.
    
    Parameters
    ----------
    comment : str
        Contains the text for the comment."""
    comment = TextAreaField('Comment', validators=[Length(min=0, max=140)])
    submit = SubmitField('Send')

class SearchForm(FlaskForm):
    """Form for searching for posts.
    
    Parameters
    ----------
    search_str : str
        Is the string used to make search queries."""
    search_str = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
