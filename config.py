import os
from dotenv import load_dotenv

# تحديد المسار الأساسي للمشروع حيث يوجد ملف .env
basedir = os.path.abspath(os.path.dirname(__file__))

# تحميل متغيرات البيئة من ملف .env
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    فئة إعدادات التطبيق الرئيسية (للتطوير والإنتاج).
    تقوم بتحميل كل الإعدادات من متغيرات البيئة وتوفر قيمًا افتراضية آمنة.
    """
    # --- إعدادات Flask الأساسية ---
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-strong-default-secret-key-for-dev'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # --- إعدادات قاعدة البيانات (SQLAlchemy) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'autoflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- إعدادات المهام الخلفية (Celery) ---
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    # --- إعدادات التطبيق المخصصة ---
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # --- مفاتيح واجهات برمجة التطبيقات (API Keys) ---
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')

    # --- إعدادات التكاملات (Integrations) ---
    SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
    SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER')


class TestConfig(Config):
    """
    فئة إعدادات خاصة ببيئة الاختبار، ترث من الفئة الرئيسية وتعدل القيم اللازمة.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True