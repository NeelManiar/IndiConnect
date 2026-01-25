from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.mentor import bp
from app.mentor.forms import WorkerProfileForm, SessionGoalForm, SessionRatingForm
from app.models import db, Worker, Mentor, MentorshipSession

# --- Helper function for checking/redirecting profile status ---
def check_profile_status():
    """Checks if the current user has completed their Worker profile."""
    if not current_user.job_title or not current_user.desired_skill:
        flash('Please complete your Career Catalyst profile to find mentors.', 'warning')
        return redirect(url_for('mentor.profile_setup'))
    return None

@bp.route('/profile-setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    """Route for the worker to set up their job title and desired skill."""
    
    # Pre-populate form with existing data
    form = WorkerProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.job_title = form.job_title.data
        current_user.desired_skill = form.desired_skill.data
        db.session.commit()
        flash('Career profile updated successfully! You can now browse mentors.', 'success')
        return redirect(url_for('mentor.index'))
        
    return render_template('mentor/profile_setup.html', title='Profile Setup', form=form)


@bp.route('/')
@login_required
def index():
    """Lists available mentors, prioritizing those matching the worker's desired skill."""
    
    # Check profile status first
    status_check = check_profile_status()
    if status_check:
        return status_check

    # 1. Get the worker's desired skill
    desired_skill = current_user.desired_skill

    # 2. Query mentors who explicitly list that skill (Best match)
    best_match_mentors = Mentor.query.filter(
        Mentor.skills.ilike(f'%{desired_skill}%')
    ).all()
    
    # 3. Query remaining mentors (General pool)
    general_mentors = Mentor.query.filter(
        ~Mentor.skills.ilike(f'%{desired_skill}%')
    ).all()
    
    mentors = best_match_mentors + general_mentors
    
    return render_template(
        'mentor/index.html', 
        title='Browse Mentors', 
        mentors=mentors,
        desired_skill=desired_skill
    )


@bp.route('/connect/<int:mentor_id>', methods=['GET', 'POST'])
@login_required
def connect(mentor_id):
    """Route for requesting a session with a specific mentor."""
    
    status_check = check_profile_status()
    if status_check:
        return status_check

    mentor = Mentor.query.get_or_404(mentor_id)
    form = SessionGoalForm()
    
    existing_session = MentorshipSession.query.filter_by(
        worker_id=current_user.id,
        mentor_id=mentor_id,
        status='Pending'
    ).first()
    
    if existing_session:
        flash('You already have a pending session request with this mentor.', 'info')
        return redirect(url_for('mentor.index'))
    
    if form.validate_on_submit():
        session = MentorshipSession(
            worker_id=current_user.id,
            mentor_id=mentor.id,
            goal=form.goal.data,
            status='Pending'
        )
        db.session.add(session)
        db.session.commit()
        flash(f'Mentorship request sent to {mentor.username} successfully!', 'success')
        return redirect(url_for('mentor.session_status'))
        
    return render_template(
        'mentor/connect.html', 
        title='Request Session', 
        form=form, 
        mentor=mentor
    )


@bp.route('/sessions')
@login_required
def session_status():
    """Displays the worker's active and completed mentorship sessions."""
    
    # Fetch all sessions for the current worker
    sessions = MentorshipSession.query.filter_by(worker_id=current_user.id).order_by(MentorshipSession.timestamp.desc()).all()
    
    return render_template('mentor/session_status.html', title='My Sessions', sessions=sessions)


@bp.route('/rate/<int:session_id>', methods=['GET', 'POST'])
@login_required
def rate_session(session_id):
    """Allows the worker to rate a completed session."""
    
    session = MentorshipSession.query.get_or_404(session_id)
    
    # Security check: Ensure worker owns the session and it is completed but not rated
    if session.worker_id != current_user.id or session.status != 'Completed' or session.rating is not None:
        flash('Cannot rate this session.', 'danger')
        return redirect(url_for('mentor.session_status'))
        
    form = SessionRatingForm()
    
    if form.validate_on_submit():
        session.rating = form.rating.data
        session.status = 'Rated' # Final status
        
        # Optionally, update the mentor's average rating here (future feature)
        
        db.session.commit()
        flash('Thank you for rating your mentor! Session finalized.', 'success')
        return redirect(url_for('mentor.session_status'))
        
    return render_template('mentor/rate_session.html', title='Rate Session', form=form, session=session)