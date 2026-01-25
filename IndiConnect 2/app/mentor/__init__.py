from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask import Blueprint

bp = Blueprint('mentor', __name__, url_prefix='/mentor')

from app.mentor import views, forms

class WorkerProfileForm(FlaskForm):
    """Form for workers to set up their career goals and skills."""
    job_title = StringField('Current Job Title', validators=[DataRequired(), Length(min=2, max=64)])
    desired_skill = StringField('What specific skill are you looking to develop?', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Save Profile & Find Mentors')

class SessionGoalForm(FlaskForm):
    """Form for setting the specific goal when requesting a mentorship session."""
    goal = TextAreaField('Define your SMART Goal for this mentorship:', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Start Session')

class SessionRatingForm(FlaskForm):
    """Form for workers to rate their mentor after session completion."""
    rating = IntegerField('Rate your Mentor (1-5 Stars):', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating & Complete')