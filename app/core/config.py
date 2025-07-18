import os
from dotenv import load_dotenv

# تحديد المسار الأساسي للمشروع
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# تحميل ملف .env من المسار الأساسي
load_dotenv(os.path.join(basedir, '.env'))

class Settings:
    """
    فئة مركزية لتجميع كل إعدادات التطبيق من متغيرات البيئة.
    توفر قيمًا افتراضية آمنة في حال عدم وجود متغيرات معينة.
    """

    # --- إعدادات Flask الأساسية ---
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'a-very-strong-default-secret-key-for-dev')
    FLASK_DEBUG: bool = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # --- إعدادات قاعدة البيانات ---
    # استخدام المسار النسبي لإنشاء قاعدة البيانات داخل مجلد 'instance'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'autoflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # --- إعدادات JWT (JSON Web Token) ---
    # هذه الإعدادات ستكون مهمة إذا قررت بناء API تعتمد على التوكن
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 60))

    # --- إعدادات المستخدمين ---
    ADMIN_EMAIL: str = os.environ.get('ADMIN_EMAIL')

    # --- مفاتيح واجهات برمجة التطبيقات (API Keys) ---
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY')
    ELEVENLABS_API_KEY: str = os.environ.get('ELEVENLABS_API_KEY')
    SERPAPI_API_KEY: str = os.environ.get('SERPAPI_API_KEY') # For Google Search

    # --- إعدادات التكاملات (Integrations) ---
    # Shopify
    SHOPIFY_SHOP_URL: str = os.environ.get('SHOPIFY_SHOP_URL')
    SHOPIFY_API_KEY: str = os.environ.get('SHOPIFY_API_KEY')
    SHOPIFY_API_PASSWORD: str = os.environ.get('SHOPIFY_API_PASSWORD')
    
    # Twilio for WhatsApp
    TWILIO_ACCOUNT_SID: str = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN: str = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER: str = os.environ.get('TWILIO_WHATSAPP_NUMBER')

   #redis
    CELERY_BROKER_URL: str = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND: str = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# في نهاية ملف config.py

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # قاعدة بيانات في الذاكرة
    WTF_CSRF_ENABLED = False # تعطيل CSRF في نماذج الاختبار



# إنشاء كائن واحد من الإعدادات لاستخدامه في كل التطبيق
settings = Settings()