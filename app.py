"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, DEFAULT_IMG_URL
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret-pw'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def display_user_listing():
    """ Display User Listing Page """

    return redirect('/users')

@app.get('/users')
def display_all_users():
    """ Display each user, convert their names to links to the view their page
        and have a link to add-user """

    # display all users
    users = User.query.all()

    return render_template('user_listing.html', users=users)

@app.get('/users/new')
def display_add_form():
    """ Display a form to create a new user """

    return render_template('new_user_form.html')

@app.post('/users/new')
def create_new_user():
    """ Retrieve data from form and sends user info to database """

    response = request.form
    image_url = response['image_url'] or None

    new_user = User(first_name = response['first_name'], last_name = response['last_name'],
        image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def display_user_page(user_id):
    """ Display a given user's page """

    curr_user = User.query.get_or_404(user_id)

    # Need 404 error page if user doesn't exist

    return render_template('user_detail_page.html', curr_user = curr_user)

@app.post('/users/<int:user_id>/delete/')
def delete_user(user_id):
    """Deletes the user's page"""
    user = User.query.get_or_404(user_id)
    User.query.filter_by(id = user_id).delete()

    db.session.commit()

    flash(f'User "{user.first_name} {user.last_name}" was successfully deleted.')
    return redirect('/users')

@app.get('/users/<int:user_id>/edit')
def display_edit_page(user_id):
    """ Display edit page """

    curr_user = User.query.get(user_id)
    return render_template('user_edit_page.html', curr_user = curr_user)

@app.post('/users/<int:user_id>/edit')
def update_user_profile(user_id):
    """Updates user profile with new information"""

    response = request.form

    curr_user = User.query.get(user_id)
    image_url = response['image_url'] or DEFAULT_IMG_URL
    if response['first_name']:
        curr_user.first_name = response['first_name']
    if response['last_name']:
        curr_user.last_name = response['last_name']
    if response['image_url'] or DEFAULT_IMG_URL:
        curr_user.image_url = image_url

    db.session.commit()
    return redirect('/users')





