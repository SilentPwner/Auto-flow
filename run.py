from app import create_app, db
from app.models.user import User, Plan, Subscription # استيراد كل النماذج
from app.models.content import GeneratedContent, ImageHistory
# ... استيراد باقي النماذج

# إنشاء نسخة من التطبيق باستخدام دالة المصنع
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    يجعل هذه الكائنات متاحة تلقائيًا في جلسة `flask shell`.
    مفيد جدًا للتصحيح والتفاعل المباشر مع قاعدة البيانات.
    """
    return {
        'db': db,
        'User': User,
        'Plan': Plan,
        'Subscription': Subscription,
        'GeneratedContent': GeneratedContent,
        'ImageHistory': ImageHistory
        # ... أضف باقي النماذج هنا
    }

if __name__ == '__main__':
    # هذا الجزء يعمل فقط عند تشغيل الملف مباشرة (python run.py)
    # خوادم الإنتاج مثل Gunicorn لن تقوم بتشغيل هذا الجزء
    app.run()