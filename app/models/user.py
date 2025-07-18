from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # --- صلاحيات المستخدم ---
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # --- علاقة بالاشتراك ---
    subscription = db.relationship('Subscription', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # e.g., 'Free', 'Pro', 'Business'
    price = db.Column(db.Float, nullable=False) # السعر الشهري
    
    # --- حدود الخطة ---
    word_limit = db.Column(db.Integer, default=0) # عدد الكلمات شهريًا
    image_limit = db.Column(db.Integer, default=0) # عدد الصور شهريًا
    workflow_limit = db.Column(db.Integer, default=0) # عدد مسارات العمل

    subscriptions = db.relationship('Subscription', back_populates='plan')

    def __repr__(self):
        return f'<Plan {self.name}>'
        
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime) # تاريخ انتهاء الصلاحية
    is_active = db.Column(db.Boolean, default=True)
    
    # --- معرفات بوابة الدفع ---
    stripe_subscription_id = db.Column(db.String(100), unique=True)
    
    user = db.relationship('User', back_populates='subscription')
    plan = db.relationship('Plan', back_populates='subscriptions')

    def __repr__(self):
        return f'<Subscription for User ID {self.user_id} on Plan ID {self.plan_id}>'