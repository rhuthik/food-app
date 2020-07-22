from sqlalchemy.orm import relationship
from foodapp import db, login_manager
from flask_login import UserMixin

theTable = db.Table('theTab',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingred_id', db.Integer, db.ForeignKey('ingredient.id'))
)

likeTable = db.Table('like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

dislikeTable = db.Table('dislike',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    isEmailVerified = db.Column(db.Boolean, nullable=True , default=False)
    propic = db.Column(db.String(20), default='default.jpg', nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recipes_authored = db.relationship('Recipe', backref='author', lazy=True)
    recipes_liked = db.relationship('Recipe', secondary=likeTable, back_populates='users_liked')
    recipes_disliked = db.relationship('Recipe', secondary=likeTable, back_populates='users_liked')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.propic}')"


class Ingredient(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recipes = db.relationship('Recipe', secondary=theTable, back_populates='ingredients')

    def __repr__(self):
        return f"('{self.name}')"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    procedure = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String, nullable=False, default='default.png')
    ingredients = db.relationship('Ingredient', secondary=theTable, back_populates='recipes')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    users_liked = db.relationship('User', secondary=likeTable, back_populates='recipes_liked')
    users_disliked = db.relationship('User', secondary=dislikeTable, back_populates='recipes_disliked')

    def __repr__(self):
        return f"('{self.name}')"
