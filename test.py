from flask import Flask, request, redirect, abort, url_for, render_template, make_response, session
from markupsafe import escape
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, query
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cDe#4RfV'

sql_user = {
    'user': 'dbuser',
    'password': 'P@ssw0rd',
    'host': 'localhost',
    'database': 'study1'
}

engine = create_engine("mysql+mysqlconnector://", connect_args=sql_user, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/id/<int:id>')
def hello(id):
    return f"Hello, ID:{id}!"

@app.route('/get_test')
def get_test():
    get_word = request.args.get('name', '1')
    return f"Hello, {get_word}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    message = None
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = request.form['password']
        if not username:
            error = 'Enter username.'
        elif db_session.query(User).filter_by(username=username).first() is not None:
            error = 'The username is already registered.'

        else :
            new_user = User(username=username, password=password)
            db_session.add(new_user)
            db_session.commit()
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

        elif username != 'admin':
            user = db_session.query(User).filter_by(username=username).first()
            print(user.password_hash)
            if not user or not user.check_password(password=password):
                error = 'Wrong username or password.'

            else:
                return redirect(url_for('test', username=username))

        else:
            error='Admin is not allowed.'

    return render_template('login_form.html', error=error)

@app.route('/redirect_test')
def redirect_test():
    return redirect(url_for('get_test', name='test'))

@app.route('/error_test')
def error_test():
    abort(404)

@app.route('/test')
def test():
    test_user = request.args.get('username')
    if test_user is not None :
        return f"test ok, {test_user}"

    else :
        return redirect(url_for('login'))






@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
