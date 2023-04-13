from flask import Flask, request, redirect, abort, url_for, render_template, make_response
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return "<H3>Hello, World!<H3><p>test</p>"

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
        username = request.form['username']
        if username != 'admin':
            return redirect(url_for('test', username=username))

        else error='Admin is not allowed.'

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
