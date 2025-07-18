# app/__init__.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# تهيئة الإضافات بدون تطبيق
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # تهيئة الإضافات مع التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from . import models
        from .main import bp as main_bp
        app.register_blueprint(main_bp)
        from .api.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        # ... سجل بقية الـ Blueprints

    return app
