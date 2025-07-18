from flask import Flask
from config import Config # <-- يستورد الفئة من الملف الجذري
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bootstrap_flask import Bootstrap
from flask_login import LoginManager
from app.tasks.celery_app import make_celery # استيراد دالة مصنع Celery

# تهيئة الإضافات بدون تطبيق
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    
    # تحميل الإعدادات من الكائن الذي تم تمريره
    app.config.from_object(config_class)

    # تهيئة الإضافات مع التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    # تسجيل Blueprints (المسارات)
    # ملاحظة: الاستيراد داخل الدالة يحل العديد من مشاكل الاستيراد الدائري
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ... (أضف هنا تسجيل بقية الـ Blueprints عند إنشائها) ...
    from app.api.content import bp as content_api_bp
    app.register_blueprint(content_api_bp, url_prefix='/api/content')

    # ربط Celery مع سياق التطبيق
    app.celery = make_celery(app)

    # ... (باقي الكود لصفحات الأخطاء) ...

    return app

from app.models import user # استيراد النماذج مهم لـ Flask-Migrate