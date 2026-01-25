import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config 


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bcrypt = Bcrypt()

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

from app import models

login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = 'warning'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    migrate = Migrate(app,db)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)

    from app.models import Worker

    @login.user_loader
    def load_user(id):
        """Tells Flask-Login how to find a user by their ID."""
        return Worker.query.get(int(id))

    # ==========================================================
    # Register Blueprints
    # ==========================================================

    # 1. Authentication Blueprint (Login, Register, Logout)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 2. Main Blueprint (Index, Dashboard)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # 3. Career Catalyst Blueprint (Mentor Matching)
    from app.mentor import bp as mentor_bp
    app.register_blueprint(mentor_bp)

    # 4. Stability Locator Blueprint (Resource Map)
    from app.resource import bp as resource_bp
    app.register_blueprint(resource_bp)

    # 5. Eyes on the Ground Blueprint (Feedback/Reporting)
    from app.feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp)
    
    # Imports the model files so SQLAlchemy knows about them
    with app.app_context():
        from app import models
    
    return app