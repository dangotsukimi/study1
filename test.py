from flask import Flask, request, redirect, abort, url_for, render_template, make_response, session
from markupsafe import escape
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = escape(request.form['username'])
        if username != 'admin':
            return redirect(url_for('test', username=username))

        else :
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
