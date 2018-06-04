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
    
    title = StringField('Title', validators=[Length(min=0, max=100), DataRequired()])
    topics = StringField('Tags (Can only input one currently)', validators=[DataRequired()])
    text = StringField('Text', validators=[Length(min=0, max=100)])
    link = StringField('Link', validators=[Length(min=0, max=240)])
    event = StringField('Event (optional)', validators=[Length(min=0, max=150)])
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
