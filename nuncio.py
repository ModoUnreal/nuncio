from app import db, app
from app.models import User, Post, Comment, Topic
from waitress import serve


@app.shell_context_processor
def make_shell_context():
    """Makes the shell context, allowing for specific variables, and classes
       to be known by the interactive Python session on startup."""
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'Topic': Topic}

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
