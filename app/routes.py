from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.helpers import redirect_url, get_posts_from_topic, check_if_voted
from app.models import User, Post, Comment, Topic,find_users_post
from app.forms import CommentForm, SubmitForm, SearchForm
from app import app, db


@app.route('/')
@app.route('/index')
@login_required
def index():
    """View function for the index site, basically the main site.
       Sorts posts by hotness"""
    posts = Post.query.order_by(Post.hotness.desc()).all()
    return render_template('index.html', title='Dopenet: You can do anything', posts=posts )

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """View function for the submit site, which contains a standard
       form. Creates initial variables for mutable variables like
       upvotes, downvotes and importance, to avoid any TypeErrors."""
    form = SubmitForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data, user_id=current_user.id, topics=[Topic(tag_name=form.topics.data)])
        post.upvotes = 1
        post.downvotes = 0
        post.importance = 1
        post.score = post.get_score()
        db.session.add(post)
        db.session.commit()
    
        flash('You have now made a post!')
        return redirect(url_for('index'))
    return render_template('submit.html', title='Submit', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    """View function for the user profile page. May become deprecated
       as there isn't much use for it, except for listing specific posts."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = find_users_post(user)
    return render_template('user.html', user=user, posts=posts)

@app.route('/item/<post_id>', methods=['GET', 'POST'])
def item(post_id):
    """Shows a specific item, which is specified by it's unique id.
       Also contains a basic form for submitting comments, which are
       yet to be sorted by popularity."""

    post = Post.query.filter_by(id=post_id).first_or_404()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data, post_id=post.id,
                user_id=current_user.id, username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('item', post_id=post_id))

    comments = Comment.query.filter_by(post_id=post.id)
    user = post.author
    return render_template('item.html', user=user, post=post,
            comments=comments, form=form)


@app.route('/delete_comment/<post_id>/<comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    """View function which deletes comments, specifically a POST method
       for obvious reasons."""
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment != None:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('item', post_id=post_id))


@app.route('/delete_post/<post_id>', methods=['POST'])
def delete_post(post_id):
    """View function which deletes a post."""
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/vote/<post_id>', methods=['POST'])
def vote(post_id):
    """View function which allows users to vote a post.
       Voting is allowed anywhere as long as there is a post to vote on,
       as would be expected.
       
       Uses another redirect_url() function which can be found in helpers.py"""
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        if post.upvotes == None:
            post.make_vote_int()

        if "upvote" in request.form and not check_if_voted(post, current_user):
            post.upvotes = post.upvotes + 1
            current_user.voted_on.append(post)
            db.session.commit()
            post.get_score()
            post.set_hotness()
            db.session.commit()

        if "downvote" in request.form and not check_if_voted(post, current_user):
            post.downvotes = post.downvotes + 1
            current_user.voted_on.append(post)
            db.session.commit()
            post.get_score()
            post.set_hotness()
            db.session.commit()

    return redirect(redirect_url()) # Look at snippet 62

@app.route('/give_importance/<post_id>', methods=['POST'])
def give_importance(post_id):
    """A function which allows users to give importance.
       How this works is simple. A user would give a post importance,
       thus increasing the amount of time a post is visible/popular.
       
       The catch is that the user then loses 5 of his/her own points."""
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        if post.importance == None:
            post.make_importance_int()
        post.importance = post.importance + 1
        post.set_hotness()
        db.session.commit()

    return redirect(redirect_url())


@app.route('/search', methods=['GET', 'POST'])
def search():
    """View function which takes inputted data from a search bar and passes
       it on to the search_result function, to be made into a search_query."""
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        search_str = form.search_str.data
        return redirect(url_for('search_result', search_str=str(search_str)))

    return redirect(url_for('search_result', search_str=form.search_str.data))

@app.route('/search_result/<search_str>', methods=['GET'])
def search_result(search_str):
    """Makes a post_query and a topic_query which contains any posts with
       similar names."""
    post_query = Post.query.filter_by(title=search_str).all()
    topic_query = Topic.query.filter_by(tag_name=search_str).first()

    post_with_topic = get_posts_from_topic(topic_query)

    return render_template('search_result.html', post_query=post_query, posts=post_with_topic)

@app.route('/search_topic/<topic_query>', methods=['GET'])
def search_topic(topic_query):
    """Shows a list of posts under the specific tag being queried."""
    topic = Topic.query.filter_by(id=topic_query).first()
    return render_template('topic.html', topic=topic)

@app.route('/faq', methods=['GET'])
def faq():
    """Returns the faq html file."""
    return render_template('faq.html')

@app.route('/contact', methods=['GET'])
def contact():
    """Returns the contact html file."""
    return render_template('contact.html')

@app.route('/rules', methods=['GET'])
def rules():
    """Returns the rules html file."""
    # Should "be substantial" be a rule/motto?
    return render_template('rules.html')

