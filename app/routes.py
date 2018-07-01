from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.helpers import redirect_url, get_posts_from_topic, check_if_upvoted, check_if_downvoted, check_topic_exists, check_if_given_importance, check_event_exists
from app.decorators import update_user
from app.models import User, Post, Comment, Topic, Event, find_users_post
from app.forms import CommentForm, SubmitForm, SearchForm
from app import app, db
import datetime


@app.route('/')
@app.route('/index')
def index():
    """View function for the index site, basically the main site.
       Sorts posts by hotness"""
    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.hotness.desc())
    for post in posts:
        post.set_age()
        post.get_hotness()

    posts = Post.query.order_by(Post.hotness.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
            if posts.has_prev else None

    return render_template('index.html', title='Fair news, chosen by you.',
            posts=posts.items, check_if_upvoted=check_if_upvoted,
            check_if_downvoted=check_if_downvoted, next_url=next_url, prev_url=prev_url)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
@update_user
def submit():
    """View function for the submit site, which contains a standard
       form. Creates initial variables for mutable variables like
       upvotes, downvotes and importance, to avoid any TypeErrors."""
    form = SubmitForm()
    if form.validate_on_submit():

        if check_event_exists(form.event.data):
            event = Event.query.filter_by(event_name=form.event.data).first()

        elif not check_event_exists(form.event.data):
            event = Event(event_name=form.event.data)

        # Checks whether the topic exists, so as to not make identical topics.
        if check_topic_exists(form.topics.data):
            topic = Topic.query.filter_by(tag_name=form.topics.data).first()
            post = Post(title=form.title.data, text=form.text.data, user_id=current_user.id, topics=[topic],
                    event=event)

        elif not check_topic_exists(form.topics.data):
            post = Post(title=form.title.data, text=form.text.data,
                    user_id=current_user.id,
                    topics=[Topic(tag_name=form.topics.data)],
                    event=event)

        # Checks to see if post is link or url.
        if form.link.data == "":
            post.is_link = False

        else:
            post.is_link = True

        if form.link.data == "" and form.text.data == "":
            flash("Please input either a link or text, or both.")
            return redirect(url_for('submit'))

        post.upvotes = 1
        post.link = form.link.data
        post.downvotes = 0
        post.importance = 10
        post.timestamp = datetime.datetime.utcnow()
        post.hotness = post.get_hotness()
        post.score = post.get_score()
        db.session.add(post)
        db.session.commit()
    
        flash('You have now made a post!')
        return redirect(url_for('index'))
    return render_template('submit.html', title='Submit', form=form)

@app.route('/user/<username>')
def user(username):
    """View function for the user profile page. May become deprecated
       as there isn't much use for it, except for listing specific posts."""
    user = User.query.filter_by(username=username).first_or_404()
    posts = find_users_post(user)

    for post in posts:
        post.set_age()

    return render_template('user.html', user=user, posts=posts, check_if_upvoted=check_if_upvoted,
            check_if_downvoted=check_if_downvoted)

@app.route('/item/<post_id>', methods=['GET', 'POST'])
def item(post_id):
    """Shows a specific item, which is specified by it's unique id.
       Also contains a basic form for submitting comments, which are
       yet to be sorted by popularity."""

    post = Post.query.filter_by(id=post_id).first_or_404()

    post.set_age()

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
            comments=comments, form=form, check_if_upvoted=check_if_upvoted,
            check_if_downvoted=check_if_downvoted)


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
@login_required
def vote(post_id):
    """View function which allows users to vote a post.
       Voting is allowed anywhere as long as there is a post to vote on,
       as would be expected.
       
       Uses another redirect_url() function which can be found in helpers.py"""
    post = Post.query.filter_by(id=post_id).first()
    if post != None:
        if post.upvotes == None:
            post.make_vote_int()
            post.author.sum_post_scores()
            db.session.commit()

        if "upvote" in request.form and not check_if_upvoted(post, current_user):

            post.upvotes = post.upvotes + 1
 
            current_user.upvoted_on.append(post)

            if check_if_downvoted(post, current_user):
                post.downvotes = post.downvotes - 1
                current_user.downvoted_on.remove(post)

            post.get_score()
            post.get_hotness()
            post.author.sum_post_scores()
            db.session.commit()

        if "downvote" in request.form and not check_if_downvoted(post, current_user):
            post.downvotes = post.downvotes + 1
            current_user.downvoted_on.append(post)

            if check_if_upvoted(post, current_user):
                post.upvotes = post.upvotes - 1
                current_user.upvoted_on.remove(post)

            post.get_score()
            post.get_hotness()
            post.author.sum_post_scores()
            db.session.commit()

    return redirect(redirect_url()) # Look at snippet 62

@app.route('/give_importance/<post_id>', methods=['POST'])
@login_required
def give_importance(post_id):
    """A function which allows users to give importance.
       How this works is simple. A user would give a post importance,
       thus increasing the amount of time a post is visible/popular.
       
       The catch is that the user then loses 5 of his/her own points."""
    post = Post.query.filter_by(id=post_id).first()
    if post != None and not check_if_given_importance(post, current_user):

        if post.importance == None:
            post.make_importance_int()

        post.importance = post.importance + 1

        current_user.importance_debt = current_user.importance_debt + 5

        current_user.given_importance_to.append(post)
        current_user.scores = current_user.sum_post_scores()
        post.hotness = post.get_hotness()
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
    user_query = User.query.filter_by(username=search_str).first()

    post_with_topic = get_posts_from_topic(topic_query)

    for post in post_query:
        post.set_age()

    for post in post_with_topic:
        post.set_age()

    return render_template('search_result.html', post_query=post_query,
            posts=post_with_topic, user=user_query, check_if_upvoted=check_if_upvoted, check_if_downvoted=check_if_downvoted)

@app.route('/search_topic/<topic_query>', methods=['GET'])
def search_topic(topic_query):
    """Shows a list of posts under the specific tag being queried."""
    topic = Topic.query.filter_by(tag_name=topic_query).first()
    return render_template('topic.html', topic=topic, check_if_upvoted=check_if_upvoted,
            check_if_downvoted=check_if_downvoted)

@app.route('/event/<event_query>', methods=['GET'])
def search_event(event_query):
    """Shows a list of events under the specific event being queried."""
    event = Event.query.filter_by(event_name=event_query).first()
    return render_template('event.html', event=event, check_if_upvoted=check_if_upvoted,
            check_if_downvoted=check_if_downvoted)

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

@app.route('/about', methods=['GET'])
def about():
    """Returns the about html file."""
    return render_template('about.html')

@app.route('/contributing', methods=['GET'])
def contributing():
    """Returns the contributing html file."""
    return render_template('contributing.html')

@app.route('/feature-request', methods=['GET'])
def feature_request():
    """Returns the feature_request html file."""
    topic = Topic.query.filter_by(tag_name="feature-request").first()

    return render_template('feature-request.html', topic=topic, check_if_downvoted=check_if_downvoted, check_if_upvoted=check_if_upvoted)
