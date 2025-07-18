# app/tasks/workflow_tasks.py
from .celery_app import celery
from app.services import automation_service # استيراد الخدمة التي تحتوي على المنطق
import time

@celery.task(name="tasks.execute_workflow")
def execute_workflow_task(workflow_id: int):
    """
    (M18) - مهمة Celery لتنفيذ سير عمل معين.
    يتم استدعاؤها من طبقة الـ API أو Services.
    """
    print(f"Starting execution for workflow {workflow_id} in the background...")
    try:
        # استدعاء الخدمة التي تحتوي على المنطق الفعلي
        result = automation_service.execute_workflow(workflow_id)
        print(f"Workflow {workflow_id} completed with result: {result}")
        return {"status": "SUCCESS", "result": result}
    except Exception as e:
        # تسجيل الخطأ بشكل مناسب
        print(f"Error executing workflow {workflow_id}: {e}")
        return {"status": "FAILURE", "error": str(e)}

@celery.task(name="tasks.scheduled_workflow_check")
def scheduled_workflow_check():
    """
    مهمة دورية (Periodic Task) للتحقق من وجود مسارات عمل مجدولة.
    يمكن تهيئتها لتعمل كل دقيقة باستخدام Celery Beat.
    """
    print("Checking for scheduled workflows...")
    # 1. ابحث في قاعدة البيانات عن مسارات العمل التي لديها محفز من نوع 'schedule'
    # 2. إذا حان وقت تشغيل أحدها، قم باستدعاء execute_workflow_task.delay(workflow.id)
    return "Scheduled check complete."