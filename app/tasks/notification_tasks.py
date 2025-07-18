# app/tasks/notification_tasks.py
from .celery_app import celery

# يفترض وجود خدمة لإرسال البريد الإلكتروني
# from app.services import email_service

@celery.task(name="tasks.send_email_async")
def send_email_async(recipient: str, subject: str, body: str):
    """
    مهمة لإرسال البريد الإلكتروني في الخلفية لتجنب إبطاء استجابة الويب.
    """
    print(f"Sending email to {recipient} with subject '{subject}'...")
    try:
        # email_service.send(to=recipient, subject=subject, body=body)
        # محاكاة للإرسال
        import time
        time.sleep(2) 
        print("Email sent.")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
        return {"status": "FAILURE", "error": str(e)}

@celery.task(name="tasks.send_notification")
def send_notification(user_id: int, message: str):
    """
    مهمة لإرسال إشعار داخل التطبيق أو عبر WebSocket.
    """
    print(f"Sending in-app notification to user {user_id}: '{message}'")
    # هنا تضع منطق حفظ الإشعار في قاعدة البيانات
    return {"status": "SENT"}