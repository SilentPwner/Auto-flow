from flask import Flask
from config import Config # يستورد فئة الإعدادات من الملف الجذري
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# =============================================================================
#  تهيئة الإضافات (Extensions Initialization)
# =============================================================================
# نقوم بإنشاء كائنات الإضافات هنا في النطاق العام (global scope)
# ولكن بدون ربطها بأي تطبيق بعد.
# هذا يمنع مشاكل الاستيراد الدائري.

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# إعدادات Flask-Login
login_manager.login_view = 'auth.login'  # اسم الـ blueprint والمسار
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info' # فئة CSS لرسائل Bootstrap


# =============================================================================
#  دالة مصنع التطبيق (Application Factory Function)
# =============================================================================
# هذه هي الوظيفة الرئيسية التي تبني وتربط كل أجزاء التطبيق معًا.

def create_app(config_class=Config):
    """
    يقوم بإنشاء وتهيئة تطبيق Flask.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # 1. تحميل الإعدادات من كائن Config
    app.config.from_object(config_class)

    # 2. ربط الإضافات التي تم إنشاؤها أعلاه بالتطبيق الحالي
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 3. تسجيل الـ Blueprints (مجموعات المسارات)
    #    نضع الاستيرادات داخل الدالة لتجنب مشاكل الاستيراد المبكرة.
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api.content import bp as content_api_bp
    app.register_blueprint(content_api_bp, url_prefix='/api/content')
    
    # ... (هنا يمكنك إضافة تسجيل بقية الـ Blueprints في المستقبل) ...


    # 4. تسجيل معالجات الأخطاء المخصصة (Custom Error Handlers)
    #    (هذه الخطوة اختيارية لكنها جيدة لتجربة المستخدم)
    # from .errors import bp as errors_bp
    # app.register_blueprint(errors_bp)

    return app

# =============================================================================
#  استيراد النماذج (Import Models)
# =============================================================================
# هذا الاستيراد في الأسفل مهم لكي تتعرف أدوات مثل Flask-Migrate
# على نماذج قاعدة البيانات الخاصة بك. لا تحذفه.
from app.models import user, content # أضف كل ملفات النماذج هنا
