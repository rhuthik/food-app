from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = '7976b37fadec64fb4ceae186f7533ec4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from foodapp import routes

if __name__ == '__main__':
	manager.run()