from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(id):
    return Worker.query.get(int(id))

# --- 1. The Worker Model (Extended for Career Catalyst) ---
class Worker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    
    # Career Catalyst Fields
    job_title = db.Column(db.String(64))
    location = db.Column(db.String(128))
    desired_skill = db.Column(db.String(128))

    # Relationships
    sessions = db.relationship('MentorshipSession', backref='worker', lazy='dynamic', foreign_keys='MentorshipSession.worker_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Worker {self.username}>'

# --- 2. The Mentor Model ---
class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    profession = db.Column(db.String(128))       
    skills_offered = db.Column(db.String(256))   
    availability = db.Column(db.String(128))   
    is_verified = db.Column(db.Boolean, default=False)

    # Relationships
    sessions = db.relationship('MentorshipSession', backref='mentor', lazy='dynamic', foreign_keys='MentorshipSession.mentor_id')

    def __repr__(self):
        return f'<Mentor {self.name} ({self.profession})>'

# --- 3. The Mentorship Session Model ---
class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys linking to Worker and Mentor
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))

    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(64), default='Pending') 
    goal = db.Column(db.String(256))                     
    worker_rating = db.Column(db.Integer)               
    
    def __repr__(self):
        return f'<Session {self.id} - Status: {self.status}>'