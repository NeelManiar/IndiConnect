from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class WorkerProfileForm(FlaskForm):
    """Form for workers to set up their career goals and skills."""
    job_title = StringField(
        'Current Job Title', 
        validators=[DataRequired(), Length(min=2, max=64)],
        description='Your current or most recent job title.'
    )
    desired_skill = SelectField('What specific skill are you looking to develop?', choices=[
        ('', 'Select a skill...'),
        ('communication', 'Effective Communication'),
        ('leadership', 'Leadership & Management'),
        ('coding', 'Software Engineering/Coding'),
        ('data_analysis', 'Data Analysis & SQL'),
        ('project_mgmt', 'Project Management (PMP/Agile)'),
        ('digital_marketing', 'Digital Marketing & SEO'),
        ('public_speaking', 'Public Speaking'),
        ('critical_thinking', 'Critical Thinking & Problem Solving'),
        ('negotiation', 'Negotiation & Conflict Resolution'),
        ('emotional_intel', 'Emotional Intelligence'),
        ('financial_literacy', 'Financial Literacy & Budgeting'),
        ('time_mgmt', 'Time Management & Productivity'),
        ('networking', 'Professional Networking'),
        ('ux_design', 'UX/UI Design Principles'),
        ('cloud_computing', 'Cloud Computing (AWS/Azure)'),
        ('cybersecurity', 'Cybersecurity Awareness'),
        ('ai_literacy', 'AI & Machine Learning Basics'),
        ('sales_strategy', 'Sales & Persuasion'),
        ('writing', 'Technical & Business Writing'),
        ('foreign_lang', 'Foreign Language Proficiency')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Save Profile & Find Mentors')


class SessionGoalForm(FlaskForm):
    """Form for setting the specific goal when requesting a mentorship session."""
    goal = TextAreaField(
        'Define your SMART Goal for this mentorship:', 
        validators=[DataRequired(), Length(max=500)],
        description='Specific, Measurable, Achievable, Relevant, Time-bound goal.'
    )
    submit = SubmitField('Request Mentorship Session')

class SessionRatingForm(FlaskForm):
    """Form for workers to rate their mentor after session completion."""
    rating = IntegerField(
        'Rate your Mentor (1-5 Stars):', 
        validators=[DataRequired(), NumberRange(min=1, max=5)],
        description='1 = Poor, 5 = Excellent'
    )
    submit = SubmitField('Submit Rating & Complete')