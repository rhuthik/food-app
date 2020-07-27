from sqlalchemy.orm import relationship
from foodapp import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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

favoritesTable = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    isEmailVerified = db.Column(db.Boolean, nullable=True , default=False)
    propic = db.Column(db.String(20), default='default.png', nullable=False)
    password = db.Column(db.String(60), nullable=False)
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    recipes_authored = db.relationship('Recipe', backref='author', lazy=True)
    favorite_recipes = db.relationship('Recipe', secondary=favoritesTable, back_populates='users_favorite')
    recipes_liked = db.relationship('Recipe', secondary=likeTable, back_populates='users_liked')
    recipes_disliked = db.relationship('Recipe', secondary=dislikeTable, back_populates='users_disliked')

    def get_token(self, expires_sec=300) :
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({ 'user_id' : self.id }).decode('utf-8')

    @staticmethod
    def verify_token(token) :
        s = Serializer(app.config['SECRET_KEY'])
        try :
            user_id = s.loads(token)['user_id']
        except :
            return None
        return User.query.get(user_id)

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
    users_favorite = db.relationship('User', secondary=favoritesTable, back_populates='favorite_recipes')
    users_liked = db.relationship('User', secondary=likeTable, back_populates='recipes_liked')
    users_disliked = db.relationship('User', secondary=dislikeTable, back_populates='recipes_disliked')

    def __repr__(self):
        return f"('{self.name}')"
