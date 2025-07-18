# app/services/strategy_service.py
from . import ai_service # يمكن للخدمات استدعاء بعضها البعض
from app.models.strategy import MarketingPlan
from app import db

def create_marketing_plan(user_id: int, project_data: dict) -> dict:
    """
    (M15) يولد خطة تسويق استراتيجية.
    """
    # 1. بناء Prompt عملاق ومفصل من بيانات المشروع
    prompt = f"Create a detailed 3-month marketing plan for a project with this description: {project_data.get('description')}..."
    
    # 2. استدعاء خدمة الـ AI (إعادة استخدام المنطق)
    # لا نستدعي OpenAI مباشرة، بل نستخدم خدمتنا المعزولة
    plan_text = ai_service.openai_api.get_chat_completion(prompt, model="gpt-4") # قد نستخدم نموذج أقوى هنا
    
    # 3. تحليل النص وتحويله إلى JSON منظم
    plan_data = {"executive_summary": "...", "monthly_plan": {}}
    
    # 4. حفظ الخطة في قاعدة البيانات
    new_plan = MarketingPlan(
        user_id=user_id,
        project_name=project_data.get('name'),
        generated_plan_data=plan_data
    )
    db.session.add(new_plan)
    db.session.commit()
    
    return plan_data

def forecast_trends(industry: str) -> list:
    """
    (M17) Placeholder للتنبؤ بالاتجاهات.
    """
    # 1. استدعاء google_search_api (Google Trends) وتويتر API
    # 2. تحليل البيانات لتحديد المواضيع الصاعدة
    return [{"trend": "Sustainable Packaging", "momentum": "high"}]