from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Worker, Mentor 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = Worker.query.filter_by(username=username.data).first()
        if user: raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = Worker.query.filter_by(email=email.data).first()
        if user: raise ValidationError('Email already registered.')

class MentorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    job_title = StringField('Current Job Title', validators=[DataRequired()])
    skills_offered = TextAreaField('Expertise', validators=[DataRequired()])
    submit = SubmitField('Become a Mentor')

    def validate_username(self, username):
        worker = Worker.query.filter_by(username=username.data).first()
        mentor = Mentor.query.filter_by(username=username.data).first()
        if worker or mentor: raise ValidationError('Username already in use.')

    def validate_email(self, email):
        worker = Worker.query.filter_by(email=email.data).first()
        mentor = Mentor.query.filter_by(email=email.data).first()
        if worker or mentor: raise ValidationError('Email already registered.')