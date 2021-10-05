from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from a.model import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
    	validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
    	validators=[DataRequired(), Length(min=2, max=30)])
   
    password = PasswordField('Password',
    	validators=[DataRequired()])
    age = StringField('Age',
        validators=[DataRequired()])
    phonenumber = StringField('Phone Number',
        validators=[DataRequired()])

    city = StringField('City',
        validators=[DataRequired(), Length(min=2, max=20)])

    confirm_password = PasswordField('Confirm Password',
    	validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exit')


class LoginForm(FlaskForm):
    username = StringField('Username',
    	validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
    	validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])

    firstname = StringField('First Name',
        validators=[DataRequired(), Length(min=2, max=20)])

    lastname = StringField('Last Name',
        validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
        validators=[DataRequired(), Length(min=2, max=30)])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
   
    age = StringField('Age',
        validators=[DataRequired()])

    phonenumber = StringField('Phone Number',
        validators=[DataRequired()])

    city = StringField('City',
        validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Save')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exit')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')