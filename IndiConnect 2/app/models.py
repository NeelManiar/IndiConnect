from app import db, login 
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# --- Worker Model (User Model) ---
class Worker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    
    job_title = db.Column(db.String(64))
    desired_skill = db.Column(db.String(128))
    
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    sessions = db.relationship('MentorshipSession', backref='worker', lazy='dynamic', foreign_keys='MentorshipSession.worker_id')

    def __repr__(self):
        return f'<Worker {self.username}>'

# --- Mentor Model ---
class Mentor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True) 
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    
    # New Mentor fields
    skills = db.Column(db.Text) 
    job_title = db.Column(db.String(128))
    
    is_approved = db.Column(db.Boolean, default=True) 
    
   
    def __repr__(self):
        return f'<Mentor {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- Mentorship Session Model ---
class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    
    goal = db.Column(db.String(500))
    status = db.Column(db.String(20), default='Pending') 
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Session {self.id} Status: {self.status}>'

# --- Feedback Report Model ---
class FeedbackReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    category = db.Column(db.String(50))
    location_details = db.Column(db.String(100))
    description = db.Column(db.String(500))
    severity = db.Column(db.String(20))
    status = db.Column(db.String(20), default='New Report')
    resolution_details = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)

# --- MENTORSHIP MODEL ---
class MentorshipMatch(db.Model):
    __tablename__ = 'mentorship_match'
    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.String(100))
    topic = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Active')
    
    user_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- RESOURCE ALERT MODEL ---
class ResourceAlert(db.Model):
    __tablename__ = 'resource_alert'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    message = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    type = db.Column(db.String(64)) 
    address = db.Column(db.String(256))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(32))
    hours = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Report {self.name}>'


@login.user_loader
def load_user(id):
    worker = Worker.query.get(int(id))
    if worker:
        return worker
        
    mentor = Mentor.query.get(int(id))
    if mentor:
        return mentor
        
    return None