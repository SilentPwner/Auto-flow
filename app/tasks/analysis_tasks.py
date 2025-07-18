# app/tasks/analysis_tasks.py
from .celery_app import celery
from app.services import analytics_service, seo_service

@celery.task(name="tasks.generate_seo_report_async")
def generate_seo_report_async(user_id: int, keyword: str):
    """
    (M11) - مهمة لتوليد تقرير SEO في الخلفية لأنها قد تستغرق وقتاً.
    """
    print(f"Generating SEO report for keyword '{keyword}' for user {user_id}...")
    try:
        report = seo_service.create_seo_report_for_keyword(user_id, keyword)
        # بعد الانتهاء، يمكنك إرسال إشعار للمستخدم
        # notification_tasks.send_notification.delay(user_id, "Your SEO report is ready!")
        return {"status": "SUCCESS", "report_data": report}
    except Exception as e:
        print(f"Error generating SEO report for '{keyword}': {e}")
        return {"status": "FAILURE", "error": str(e)}

@celery.task(name="tasks.run_daily_ad_analysis")
def run_daily_ad_analysis():
    """
    (M22) - مهمة دورية لتحليل أداء الإعلانات لجميع المستخدمين الذين ربطوا حساباتهم.
    """
    print("Running daily ad performance analysis...")
    # 1. جلب قائمة بجميع المستخدمين الذين لديهم تكامل إعلاني نشط
    # 2. لكل مستخدم، قم باستدعاء analytics_service.analyze_ad_campaigns(user.id)
    return "Daily ad analysis complete."