# app/tasks/celery_app.py
from celery import Celery

# إنشاء كائن Celery بدون تطبيق. سيتم تهيئته لاحقًا.
celery = Celery(__name__,
    broker='redis://localhost:6379/0', # يمكنك وضع القيم الافتراضية هنا
    backend='redis://localhost:6379/0',
    include=[
        'app.tasks.workflow_tasks',
        'app.tasks.analysis_tasks',
        'app.tasks.notification_tasks'
    ]
)

# هذه المهمة المخصصة مهمة جدًا
# تضمن أن أي مهمة تعمل داخل سياق تطبيق Flask الصحيح
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        # يجب أن يتم ربط التطبيق بالمهمة عند تهيئة Celery
        if not hasattr(self, 'app'):
            raise RuntimeError('Task must have an app context. Did you forget to initialize Celery with the app?')
        with self.app.app_context():
            return self.run(*args, **kwargs)

# استبدال فئة المهمة الافتراضية بفئتنا المخصصة
celery.Task = ContextTask
