from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import json

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = '7976b37fadec64fb4ceae186f7533ec4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from foodapp import routes