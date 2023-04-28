import secrets
import re
from datetime import timedelta, datetime
from flask import Flask, request, redirect, abort, url_for, render_template, make_response, session
from markupsafe import escape
from models import User, db

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dbuser:P%40ssw0rd@localhost/study1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
        if not username or not password:
            error = 'Enter both username and password.'

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
                response = make_response(redirect(url_for('test')))
                expires = datetime.now() + timedelta(minutes=5)
                response.set_cookie('username', username, expires=expires)
                return response

        else:
            error='Admin is not allowed.'

    if request.cookies.get('username'):
        return redirect(url_for('test'))

    return render_template('login_form.html', error=error)

@app.route('/error_test')
def error_test():
    abort(404)

@app.route('/test')
def test():
    username = request.cookies.get('username')
    if username is not None:
        return render_template('test.html', test_user=username)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('username', '', expires=0)
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
