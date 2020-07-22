from flask_wtf import FlaskForm
from foodapp.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username) :
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError("The username has already taken please choose another one")

    def validate_email(self, email) :
        user = User.query.filter_by(email=email.name).first()
        if user :
            raise ValidationError("The email has already taken please choose another one")


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign in')
    remember = BooleanField('Remember Me')

class AddRecipe(FlaskForm):
    recipe_name = StringField('Name of Recipe', validators=[DataRequired()])
    procedure = TextField('Procedure', widget=TextArea(), validators=[DataRequired()])
    picture = FileField('Upload a picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')