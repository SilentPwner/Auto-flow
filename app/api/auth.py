from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db, login_manager
from flask_login import login_user, logout_user, current_user
from config import Config

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('هذا البريد الإلكتروني مسجل بالفعل.')
            return redirect(url_for('auth.register'))
            
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            flash('اسم المستخدم هذا موجود بالفعل.')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # Make first user admin
        if email == Config.ADMIN_EMAIL:
            new_user.is_admin = True
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('تم تسجيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.')
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
            flash('بريد إلكتروني أو كلمة مرور غير صحيحة.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/login.html', title='تسجيل الدخول')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))