from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'gt563sxkjt66eyhcof22zjl097'
db = SQLAlchemy(app)

bcryt = Bcrypt(app)

from Market import routes
