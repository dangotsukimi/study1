from flask import Flask
from markupsafe import escape
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<H3>Hello, World!<H3><p>test</p>"

@app.route('/id/<int:id>')
def hello(id):
    return f"Hello, ID:{id}!"

@app.route('/get_test')
def get_test():
    get_word = request.args.get('name', '1')
    return f"Hello, {get_word}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
