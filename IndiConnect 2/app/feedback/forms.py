from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

# --- Choices for Worker Submission Form ---

CATEGORY_CHOICES = [
    ('Safety Hazard', 'Safety Hazard'),
    ('Equipment Failure', 'Equipment Failure'),
    ('Policy Violation', 'Policy Violation'),
    ('Maintenance Request', 'Maintenance Request'),
    ('Other', 'Other')
]

SEVERITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Critical', 'Critical')
]

# --- Worker Submission Form ---

class FeedbackForm(FlaskForm):
    """Form for workers to submit anonymous feedback reports."""
    
    category = SelectField(
        'Category of Report',
        choices=CATEGORY_CHOICES,
        validators=[DataRequired()]
    )
    
    location_details = StringField(
        'Specific Location Details', 
        validators=[DataRequired(), Length(max=100)],
        description='E.g., "Dock 3 - Forklift 12", "West hallway restroom".'
    )
    
    description = TextAreaField(
        'Detailed Description of Issue', 
        validators=[DataRequired(), Length(max=500)],
        description='Please describe the issue clearly. This report is anonymous.'
    )
    
    severity = SelectField(
        'Severity Level',
        choices=SEVERITY_CHOICES,
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Submit Anonymous Report')


# --- Choices for Admin Update Form ---

ADMIN_STATUS_CHOICES = [
    ('New Report', 'New Report'),
    ('Under Review', 'Under Review'),
    ('Assigned', 'Assigned for Action'),
    ('Resolved', 'Resolved')
]

# --- Admin Update Form ---

class ReportUpdateForm(FlaskForm):
    """Form for administrators to update the status and notes of a report."""
    
    status = SelectField(
        'Update Status',
        choices=ADMIN_STATUS_CHOICES,
        validators=[DataRequired()]
    )
    
    resolution_details = TextAreaField(
        'Resolution Details/Internal Notes',
        validators=[Length(max=500)],
        description='Details on who the report was assigned to and the outcome.'
    )
    
    submit = SubmitField('Update Report Status')