from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

# Common Categories for under-recognized workers
RESOURCE_CHOICES = [
    ('', 'All Categories'),
    ('Health', 'Health Clinics'),
    ('Food', 'Food Banks & Kitchens'),
    ('Legal', 'Legal Aid & Advice'),
    ('Childcare', 'Affordable Childcare'),
    ('Financial', 'Financial Counseling'),
    ('Housing', 'Shelter & Housing Assistance'),
]

class ResourceFilterForm(FlaskForm):
    type_filter = SelectField( 
        'Filter by Type', 
        choices=RESOURCE_CHOICES, 
        validators=[DataRequired()]
    )
    submit = SubmitField('Apply Filter')