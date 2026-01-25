from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, MentorRegistrationForm
from app.models import Worker, db
from app.auth import bp as auth_bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Worker.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/login.html', title='Sign In - IndiConnect', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = RegistrationForm()
    
    if form.validate_on_submit():
        worker = Worker(username=form.username.data, email=form.email.data)
        worker.set_password(form.password.data)
        
        db.session.add(worker)
        db.session.commit()
        
        flash('Congratulations, you are now a registered worker!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register - IndiConnect', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/register/mentor', methods=['GET', 'POST'])
@bp.route('/register/mentor', methods=['GET', 'POST'])
def mentor_register():
    form = MentorRegistrationForm()
    
    if form.validate_on_submit():
        
        mentor = Mentor(
            username=form.username.data, 
            email=form.email.data, 
            job_title=form.job_title.data,
            skills=form.skills_offered.data,
            is_worker=False
        )
        mentor.set_password(form.password.data) 
        
        db.session.add(mentor)
        db.session.commit()
        
        flash('Congratulations, you are now registered as a Mentor!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template(
        'auth/mentor_register.html', 
        title='Register as Mentor', 
        form=form
    )