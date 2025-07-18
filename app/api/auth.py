from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db, login_manager # استيراد login_manager للوصول إلى user_loader
from app.models.user import User
from config import Config # استيراد Config للوصول إلى ADMIN_EMAIL

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """
    يخبر Flask-Login كيفية العثور على مستخدم معين من الـ ID المخزن في الجلسة.
    """
    return db.session.get(User, int(user_id))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('الرجاء ملء جميع الحقول.', 'danger')
            return redirect(url_for('auth.register'))

        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('هذا البريد الإلكتروني مسجل بالفعل.', 'warning')
            return redirect(url_for('auth.register'))
            
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            flash('اسم المستخدم هذا موجود بالفعل.', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # جعل أول مستخدم ببريد إلكتروني معين مديرًا
        if new_user.email == Config.ADMIN_EMAIL:
            new_user.is_admin = True
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('تم تسجيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='تسجيل حساب جديد')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('بريد إلكتروني أو كلمة مرور غير صحيحة.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        
        # توجيه المستخدم إلى الصفحة التي كان يحاول الوصول إليها قبل تسجيل الدخول
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        return redirect(next_page)
        
    return render_template('auth/login.html', title='تسجيل الدخول')


@bp.route('/logout')
def logout():
    logout_user()
    flash('تم تسجيل خروجك بنجاح.', 'info')
    return redirect(url_for('auth.login'))
