from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from extensions import db, jwt, cache, mail
from celery_app import init_celery
from flask_cors import CORS
from models import User
from werkzeug.security import generate_password_hash
from celery.schedules import crontab

celery = None



def create_admin():
    admin = User.query.filter_by(email='admin@local').first()
    if not admin:
        password = generate_password_hash('123456')
        admin = User(full_name='Admin',email='admin@local', password_hash=password, role='admin')
        db.session.add(admin)
        db.session.commit()
        return {"msg": "admin created successfully!"}
    else:
        return {"msg":"admin exists"}
    
def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)
    # CORS(app, origins=["http://localhost:5173/"])


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["JWT_SECRET_KEY"] = "super-secret"
    # ============================
    # Flask-Mail Configuration
    # ============================
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_DEFAULT_SENDER'] = 'rajnish@local'


    # ============================
    # Flask-Caching with Redis
    # ============================
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 1
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60


    # ============================
    # Celery Configuration
    # ============================
    app.config['broker_url'] = 'redis://localhost:6379/0'
    app.config['result_backend'] = 'redis://localhost:6379/0'
    app.config['timezone'] = 'Asia/Kolkata'
    app.config['beat_schedule'] = {
        # 'monthly-report': {
        #     'task': 'tasks.monthly_report',
        #     'schedule': crontab(day_of_month=26, hour=8, minute=29),
        # },
        'daily-reminder': {
            'task': 'tasks.daily_reminder',
            'schedule': crontab(),  # Every day at 8:30 AM
        },
    }


    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    global celery
    celery = init_celery(app)
    import backend_tasks
    
    from controllers import register_routes
    register_routes(api)

    return app

app = create_app()

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == "__main__":
    app.run(debug=True)