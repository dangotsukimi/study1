import secrets
import re
from flask import Flask, request, redirect, abort, url_for, render_template, make_response, session
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dbuser:P%40ssw0rd@localhost/study1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def is_valid_password(password):
    pattern = r'^[\w!@#$%&?_]+$'
    return bool(re.match(pattern, password))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    message = None
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = request.form['password']
        if not username:
            error = 'Enter username.'

        elif not username.isalnum():
            error = 'Username can only alphabet or number characters.'

        elif not is_valid_password(password):
            error = 'Passwords can only contain alphanumeric characters or the following symbols:!@#$%&?_'

        elif User.query.filter_by(username=username).first() is not None:
            error = 'The username is already registered.'

        else :
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            message = 'User has been registered.'
            return render_template('register.html', error=error, message=message)
    return render_template('register.html', error=error, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = request.form['password']

        if not username or not password:
            error = 'Enter both username and password.'

        elif not username.isalnum():
            error = 'Username can only alphabet or number characters.'

        elif not is_valid_password(password):
            error = 'Wrong username or password.'

        elif username != 'admin':
            user = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password=password):
                error = 'Wrong username or password.'

            else:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('test'))

        else:
            error='Admin is not allowed.'

    if 'logged_in' in session:
        return redirect(url_for('test'))

    return render_template('login_form.html', error=error)

@app.route('/error_test')
def error_test():
    abort(404)

@app.route('/test')
def test():
    if 'logged_in' in session:
        test_user = session['username']
        if test_user is not None:
            return render_template('test.html', test_user=test_user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
