import json
from flask import Flask, render_template, redirect
from flask import request, jsonify, abort, url_for
from flask import flash

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, NoResultFound

from flask_login import login_required, current_user
from flask_login import logout_user, login_user

from models import User, Note, setup_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    setup_db(app)
    # print(app.app_context())


@app.route('/')
def homepage():
    """Method to display homepage"""
    return render_template('views/index.html')


@app.route('/login', methods=['GET'])
def display_login():  # put application's code here
    """Method to display login form"""
    error = None
    return render_template('forms/login.html', error=error)


@app.route('/signup')
def display_signup():  # put application's code here
    """Method to display signup form"""
    error = None
    return render_template('forms/signup.html', error=error)


@app.route('/dashboard')
@login_required
def display_dashboard():
    """Method to display a user's dashboard"""
    try:
        notes = Note.query.filter_by(author_id=current_user.id).all()
        notes_list = []
        for n in notes:
            note = {
                'name': n.title,
                'body': n.body,
                'id': n.id
            }
            notes_list.append(note)
            print(notes_list)
        text = f"{len(notes)} notes"
    except:
        text = "Create a new note"
    return render_template('views/dashboard.html', name=current_user.name, text=text, notes=notes)


@app.route('/note/<int:note_id>')
@login_required
def display_note(note_id):
    """Method to display a user's dashboard"""
    result = Note.query.filter_by(author_id=current_user.id, id=note_id).first()
    note = {
        'title': result.title,
        'body': result.body,
        'id': result.id
    }
    return render_template('views/note.html', note=note)


@app.route('/create-note')
@login_required
def display_note_form():
    return render_template('forms/note.html')


@app.route('/note', methods=['POST'])
@login_required
def add_note():
    """Method to create a new post"""
    title = request.form['title']
    body = request.form['body']
    author_id = current_user.id

    note = Note(title=title, body=body, author_id=author_id)
    note.insert()

    return redirect(url_for('display_dashboard'))


@app.route('/login', methods=['POST'])
def login():
    error = f'Invalid credentials'

    email = request.form['email']
    password = request.form['password']

    try:
        user = User.query.filter_by(email=email).first()
        if user.password:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('display_dashboard'))
            else:
                error = "Invalid credentials"
                return render_template('forms/login.html', error=error)
        else:
            error = 'Email not registered'
            flash("Invalid credentials")
            return render_template('forms/login.html', error=error)
    except NoResultFound:
        error = "No result found"
        return render_template('forms/login.html', error=error)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('homepage'))


@app.route('/create_user', methods=['POST'])
def create_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    hashed_pass = generate_password_hash(password)
    try:
        user = User(name=username, email=email, password=hashed_pass)
        user.insert()
        flash("Account successfully created")
        return redirect(url_for('display_login'))
    except IntegrityError:
        user.rollback()
        error = f'Email already exists'

    return render_template('forms/signup.html', error=error)

    # except Exception as e:
    #     print(repr(e))


@app.route('/note/<int:note_id>/edit')
@login_required
def display_edit_note_form(note_id):
    title = f'Edit Note'
    result = Note.query.filter_by(author_id=current_user.id, id=note_id).first()
    note = {
        'title': result.title,
        'body': result.body,
        'id': result.id
    }
    return render_template('forms/note.html', title=title, note=note)


@app.route('/note/<int:note_id>/update', methods=['POST'])
@login_required
def update_note(note_id):
    title = request.form['title']
    body = request.form['body']

    note = Note.query.filter_by(author_id=current_user.id, id=note_id).first()
    note.title = title
    note.body = body

    note.update()

    return redirect(url_for('display_dashboard'))


@app.route('/note/<int:note_id>/delete')
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(author_id=current_user.id, id=note_id).first()
    note.delete()

    return redirect(url_for('display_dashboard'))


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404
    """
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(422)
def unprocessable_entity(error):
    """
    Error handler for 422
    """
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422


if __name__ == 'main':
    app.run()
