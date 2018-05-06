from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    """Returns a reassuring html file in the event of a 404 error,
       so as to not scare any users."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Returns another reassuring html file in the event of a 500 error."""
    db.session.rollback()
    return render_template('500.html'), 500
