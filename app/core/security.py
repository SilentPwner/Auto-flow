from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

# -----------------------------------------------------------------------------
# Password Hashing Functions
# -----------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    تجزئة كلمة المرور باستخدام خوارزمية آمنة.
    يستخدم werkzeug.security المدمج مع Flask.
    """
    return generate_password_hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    التحقق من تطابق كلمة المرور العادية مع النسخة المجزأة.
    """
    return check_password_hash(hashed_password, plain_password)


# -----------------------------------------------------------------------------
# Decorators for Route Protection
# -----------------------------------------------------------------------------

def admin_required(f):
    """
    Decorator للتأكد من أن المستخدم الحالي هو مدير (admin).
    يجب استخدامه *بعد* @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التأكد أولاً من أن المستخدم مسجل دخوله
        if not current_user.is_authenticated:
            # Flask-Login سيتعامل مع هذا، لكنها حماية إضافية
            return redirect(url_for('auth.login'))
        
        # التحقق إذا كان مديرًا
        if not current_user.is_admin:
            flash('ليس لديك الصلاحية للوصول إلى هذه الصفحة.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def subscription_required(plan_level: str):
    """
    Decorator للتأكد من أن المستخدم لديه اشتراك في خطة معينة أو أعلى.
    مثال للاستخدام: @subscription_required('pro')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            # --- هذا المنطق يحتاج إلى بناء كامل لنظام الخطط ---
            #
            # 1. يجب إضافة علاقة بين User و Plan في models.py.
            # 2. يجب إنشاء جدول Plan لتخزين الخطط (free, pro, business).
            # 3. يجب أن تكون هناك وظيفة للتحقق من مستوى الخطة.
            #
            # user_plan = current_user.plan.name # 'pro'
            # required_level_index = ['free', 'pro', 'business'].index(plan_level)
            # user_level_index = ['free', 'pro', 'business'].index(user_plan)
            #
            # if user_level_index < required_level_index:
            #     flash(f'هذه الميزة تتطلب خطة {plan_level} أو أعلى.', 'warning')
            #     return redirect(url_for('main.subscription_page')) # صفحة للترقية
            #
            # --- نهاية المنطق التخيلي ---

            # في الوقت الحالي، سنسمح بالمرور كـ placeholder
            # flash('تحذير: التحقق من الاشتراك لم يتم تنفيذه بعد.', 'info')

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ملاحظة: إذا كنت ستبني واجهة برمجة تطبيقات RESTful تعتمد على JWT بشكل كامل
# (بالإضافة إلى واجهة الويب)، فستضيف وظائف إنشاء والتحقق من التوكن هنا.
# في الوقت الحالي، سنعتمد على نظام الجلسات (Sessions) الخاص بـ Flask-Login
# لأنه أبسط وأكثر ملاءمة لتطبيق ويب متكامل (Frontend + Backend).