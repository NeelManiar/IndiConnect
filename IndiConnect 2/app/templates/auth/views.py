from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db # Import the database instance
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm # Import both forms
from app.models import Worker # Import the Worker model

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # 1. Look up the worker by username
        worker = Worker.query.filter_by(username=form.username.data).first()
        
        # 2. Check if worker exists AND password is correct
        if worker is None or not worker.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # 3. Log the user in
        login_user(worker, remember=form.remember_me.data)
        
        # 4. Handle redirection after successful login (next page logic)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        flash(f'Welcome back, {worker.username}!', 'success')
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Prevent logged-in users from registering again
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create new Worker object
        worker = Worker(username=form.username.data, email=form.email.data)
        # Hash and set the password
        worker.set_password(form.password.data)
        
        # Add to database and commit
        db.session.add(worker)
        db.session.commit()
        
        flash('Congratulations, you are now a registered worker! Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth.register', title='Register', form=form)