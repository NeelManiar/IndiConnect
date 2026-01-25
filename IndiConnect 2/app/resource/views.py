from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from app.resource import bp
from app.resource.forms import ResourceFilterForm
from app.models import Resource, db

@bp.route('/')
@login_required
def index():
    form = ResourceFilterForm(request.args)
    return render_template('resource/index.html', title='Stability Locator', form=form)

@bp.route('/data')
@login_required
def resource_data():
    """API endpoint to fetch resource data based on filters."""
    
    
    type_filter = request.args.get('type')
    
    query = Resource.query.filter_by(is_verified=True)
    
    if type_filter and type_filter != '':
        query = query.filter(Resource.type == type_filter)
        
    resources = query.all()
    
    data = []
    for r in resources:
        data.append({
            'id': r.id,
            'name': r.name,
            'type': r.type,
            'lat': r.latitude,
            'lon': r.longitude,
            'popup': f"<b>{r.name}</b><br>{r.address}<br>Type: {r.type.capitalize()}",
            'color': {
                'health': 'blue', 
                'food': 'green', 
                'legal': 'red',
                'childcare': 'purple',
                'financial': 'orange'
            }.get(r.type, 'gray')
        })
        
    return jsonify(data)