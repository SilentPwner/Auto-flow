# app/tasks/celery_app.py
from celery import Celery
from app import create_app

def make_celery(app=None):
    """
    يقوم بإنشاء وتهيئة كائن Celery.
    """
    app = app or create_app()
    
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=[ # قائمة بملفات المهام التي يجب على Celery البحث فيها
            'app.tasks.workflow_tasks',
            'app.tasks.analysis_tasks',
            'app.tasks.notification_tasks'
            ]
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# إنشاء كائن Celery العام الذي سيتم استيراده في الملفات الأخرى
celery = make_celery()