from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h2> Hello AMAZING!!! </h2>'


@app.route('/about/<username>')
def about_page(username):
    return f'<h2>About something important for {username}</h2>'
