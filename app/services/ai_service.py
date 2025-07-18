# app/services/ai_service.py
from app.integrations import openai_api, elevenlabs_api # استيراد من طبقة التكاملات
from app.models.content import GeneratedContent, ImageHistory
from app import db

# --- Text Generation Services ---
def generate_content_from_smart_template(user_id: int, template_type: str, context: dict) -> str:
    """
    (M6) يبني Prompt مفصل من قالب بسيط، يستدعي OpenAI، ويسجل النتيجة.
    """
    prompt = _build_prompt_for_template(template_type, context)
    if not prompt:
        raise ValueError("Invalid template type provided.")

    # 1. استدعاء طبقة التكاملات للحصول على النتيجة
    generated_text = openai_api.get_chat_completion(prompt)
    
    # 2. تسجيل المحتوى في قاعدة البيانات (لتتبع الاستخدام والسجل)
    new_content_entry = GeneratedContent(
        user_id=user_id,
        template_used=template_type,
        prompt_text=prompt,
        result_text=generated_text,
        word_count=len(generated_text.split())
    )
    db.session.add(new_content_entry)
    db.session.commit()
    
    return generated_text

def _build_prompt_for_template(template_type: str, context: dict) -> str:
    """وظيفة مساعدة داخلية لبناء الـ Prompts."""
    if template_type == 'product_description':
        # ... (منطق بناء prompt لوصف المنتج)
        return f"..."
    elif template_type == 'instagram_post':
        # ... (منطق بناء prompt لمنشور انستغرام)
        return f"..."
    # ... (باقي القوالب)
    return ""

# --- Image Generation Services ---
def generate_image_from_prompt(user_id: int, prompt: str) -> str:
    """
    (M8) يولد صورة من نص، يحفظها (يفترض وجود خدمة تخزين)، ويسجلها.
    """
    # 1. استدعاء طبقة التكاملات لتوليد الصورة
    image_url = openai_api.generate_image(prompt) # هذه الوظيفة تحتاج للتنفيذ في openai_api.py
    
    # في تطبيق حقيقي، ستقوم بتحميل الصورة من الرابط المؤقت وتخزينها على S3 أو خدمة مشابهة
    # final_storage_url = storage_service.upload(image_url)

    # 2. تسجيل الصورة في قاعدة البيانات
    new_image_entry = ImageHistory(user_id=user_id, prompt_text=prompt, image_url=image_url)
    db.session.add(new_image_entry)
    db.session.commit()
    
    return image_url # أو final_storage_url

# --- Audio & Video Services (Placeholders) ---
def create_video_script(user_id: int, script_type: str, topic: str) -> dict:
    """
    (M13) Placeholder لتوليد نص فيديو.
    """
    # 1. بناء prompt متخصص لنصوص الفيديو
    # 2. استدعاء openai_api.get_chat_completion
    # 3. تحليل النتيجة لتكون بصيغة storyboard (JSON)
    return {"title": f"Video script for {topic}", "storyboard": []}

def create_voiceover(user_id: int, text: str, voice_id: str) -> str:
    """
    (M14) Placeholder لتحويل نص إلى صوت.
    """
    # 1. استدعاء elevenlabs_api.text_to_speech
    # 2. تخزين الملف الصوتي والحصول على رابط
    return "path/to/generated/audio.mp3"