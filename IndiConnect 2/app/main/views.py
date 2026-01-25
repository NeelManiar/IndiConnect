from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app.models import FeedbackReport, MentorshipMatch, ResourceAlert

@bp.route('/')
@bp.route('/dashboard')
@login_required 
def dashboard():
    feedback_count = FeedbackReport.query.filter_by(user_id=current_user.id).count()
    mentor_count = MentorshipMatch.query.filter_by(user_id=current_user.id).count()

    resource_count = ResourceAlert.query.count() 

    data = {
        'mentor_matches': mentor_count,
        'resource_alerts': resource_count,
        'feedback_in_progress': feedback_count
    }
    return render_template('main/dashboard.html', data=data)