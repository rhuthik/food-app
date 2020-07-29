from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import json

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = '7976b37fadec64fb4ceae186f7533ec4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'foodbytesverify@gmail.com'
app.config['MAIL_PASSWORD'] = 'Admin123@'
mail = Mail(app)

from foodapp import routes