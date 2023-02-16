import json
from flask import Flask, render_template, redirect
from flask import request, jsonify, abort, url_for
from flask import flash

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, NoResultFound

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


@app.route('/login')
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
def display_dashboard():
    """Method to display a user's dashboard"""
    return render_template('views/dashboard.html')


@app.route('/note')
def display_note():
    """Method to display a user's dashboard"""
    return render_template('views/note.html')


@app.route('/login_user', methods=['POST'])
def login_user():
    error = f'Invalid credentials'

    email = request.form['email']
    password = request.form['password']

    try:
        user = User.query.filter_by(email=email).one()

        if check_password_hash(user.password, password):
            flash("Logged In")
            return redirect(url_for('display_dashboard'))
        else:
            flash("Invalid credentials")
            return render_template('forms/login.html', error=error)

    except NoResultFound:
        return render_template('forms/login.html', error=error)


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
        return redirect(url_for('show_login'))
    except IntegrityError:
        user.rollback()
        error = f'Email already exists'

    return render_template('forms/signup.html', error=error)

    # except Exception as e:
    #     print(repr(e))


@app.route('/logout')
def logout_user():
    return redirect(url_for('homepage'))


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
