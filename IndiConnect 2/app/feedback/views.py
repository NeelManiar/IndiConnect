from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from functools import wraps # Needed to fix the AssertionError
from app.feedback import bp
from app.feedback.forms import FeedbackForm, ReportUpdateForm 
from app.models import FeedbackReport, db 

# --- Custom Decorator for Admin Access ---

def admin_required(f):
    """Decorator to restrict view access to users with is_admin=True."""
    @wraps(f) 
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
           
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Worker report submission page."""
    form = FeedbackForm()
    
    if form.validate_on_submit():
        report = FeedbackReport(
            category=form.category.data,
            location_details=form.location_details.data,
            description=form.description.data,
            severity=form.severity.data,
            user_id = current_user.id
        )
        db.session.add(report)
        db.session.commit()
        flash('Your report has been submitted anonymously. Thank you for your feedback!', 'success')
        return redirect(url_for('feedback.status'))
        
    return render_template('feedback/index.html', title='Eyes on the Ground', form=form)


@bp.route('/status')
@login_required
def status():
    """Worker view of their recent reports (simulated status for anonymous reports)."""
    
    recent_reports = FeedbackReport.query.order_by(FeedbackReport.timestamp.desc()).limit(10).all()
    
    return render_template('feedback/status.html', title='Report Status', reports=recent_reports)


@bp.route('/admin')
@admin_required
def admin_list():
    """Lists all feedback reports for administrative review."""
    
    reports = FeedbackReport.query.order_by(FeedbackReport.timestamp.desc()).all()
    
    return render_template('feedback/admin_list.html', title='Admin: All Reports', reports=reports)

@bp.route('/admin/edit/<int:report_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(report_id):
    """Allows admin to update the status and resolution notes of a specific report."""
    
    report = FeedbackReport.query.get_or_404(report_id)
    form = ReportUpdateForm()
    
    if form.validate_on_submit():
        report.status = form.status.data
        report.resolution_details = form.resolution_details.data
        db.session.commit()
        flash(f'Report #{report_id} status updated to {report.status}.', 'success')
        return redirect(url_for('feedback.admin_list'))
        
    elif request.method == 'GET':
        form.status.data = report.status
        form.resolution_details.data = report.resolution_details

    return render_template(
        'feedback/admin_edit.html', 
        title=f'Edit Report #{report_id}', 
        form=form, 
        report=report
    )

def submit():
    new_report = Feedback(
        user_id=current_user.id, 
        title=request.form.get('title'),
        status='Pending' 
    )
    db.session.add(new_report)
    db.session.commit() 
    return redirect(url_for('main.dashboard'))