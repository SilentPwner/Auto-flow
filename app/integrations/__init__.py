from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

# تهيئة الإضافات
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # توجيه المستخدم غير المسجل للدخول
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # تهيئة الإضافات مع التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    # تسجيل Blueprints (المسارات)
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api.content import bp as content_api_bp
    app.register_blueprint(content_api_bp, url_prefix='/api/content')

    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        db.create_all()

    return app

from app.models import user # استيراد النماذج لـ Flask-Migrate