from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home_page_view():
    return render_template('home.html')

