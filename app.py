import json
from flask import Flask, render_template, redirect, jsonify

app = Flask(__name__)


@app.route('/')
def homepage():  # put application's code here
    return render_template('views/index.html')


@app.route('/login')
def show_login():  # put application's code here
    return render_template('views/index.html')


@app.route('/signup')
def display_signup():  # put application's code here
    return render_template('views/index.html')


@app.route('/')
def homepage():  # put application's code here
    return render_template('views/index.html')


@app.route('/login_user')
def login_user():
    return render_template('views/dashboard.html')


@app.route('/create_user')
def create_user():
    return redirect(homepage)


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


if __name__ == '__main__':
    app.run()