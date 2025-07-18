# celery_worker.py
from app import create_app

# إنشاء تطبيق Flask لتهيئة Celery
app = create_app()

# إبقاء كائن celery متاحًا لسطر الأوامر
celery = app.celery
