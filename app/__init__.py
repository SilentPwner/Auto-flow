# app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.tasks.celery_app import celery as celery_app # استيراد كائن Celery

# تهيئة الإضافات
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # تهيئة الإضافات الأساسية
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # --- تهيئة Celery بالطريقة الصحيحة ---
    # تحديث إعدادات Celery من إعدادات التطبيق
    celery_app.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND']
    )
    # ربط سياق التطبيق بمهام Celery
    celery_app.Task.app = app

    # --- تسجيل الـ Blueprints ---
    with app.app_context():
        # استيراد وتسجيل الـ Blueprints
        from .main import bp as main_bp
        app.register_blueprint(main_bp)

        from .api.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        from .api.content import bp as content_api_bp
        app.register_blueprint(content_api_bp, url_prefix='/api/content')

        # استيراد النماذج مهم جدًا لـ Alembic (Flask-Migrate)
        from . import models

    return app
