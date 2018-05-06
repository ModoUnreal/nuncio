from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from ..models import User, Post, Comment, find_users_post
from .. import db
from . import bp
from .forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """View function to login. Uses the login form.
       If the @login_required decorator is used on a view function
       then the user will be redirected to this function."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login to Dopenet', form=form)

@bp.route('/logout')
def logout():
    """View function to log out a user."""
    logout_user()
    return redirect(url_for('index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """View function to register a new user, using the register form."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congrats!!! You are now registered to Dopenet!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
