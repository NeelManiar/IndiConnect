import os
from app import create_app, db
from app.models import Worker, Mentor
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Worker': Worker, 'Mentor': Mentor}

if __name__ == '__main__':
    with app.app_context():
        if Worker.query.count() == 0:
            from werkzeug.security import generate_password_hash
            test_worker = Worker(
                username='maria',
                email='maria@example.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(test_worker)
            db.session.commit()
            print("Test worker 'maria' created with password 'password123'")
            
    app.run(debug=True)