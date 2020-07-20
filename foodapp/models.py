from sqlalchemy.orm import relationship
from foodapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    propic = db.Column(db.String(20), default='def.jpg', nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.propic}')"

theTable = db.Table('theTab',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingred_id', db.Integer, db.ForeignKey('ingredient.id'))

)

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

    def __repr__(self):
        return f"('{self.name}')"
