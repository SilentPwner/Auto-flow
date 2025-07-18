from app import db
import datetime

class Workflow(db.Model):
    __tablename__ = 'workflows'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    
    # علاقة واحد-إلى-واحد مع المحفز (Trigger)
    trigger = db.relationship('Trigger', back_populates='workflow', uselist=False, cascade="all, delete-orphan")
    # علاقة واحد-إلى-متعدد مع الإجراءات (Actions)
    actions = db.relationship('Action', back_populates='workflow', cascade="all, delete-orphan")
    
    user = db.relationship('User')

class Trigger(db.Model):
    __tablename__ = 'triggers'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    
    trigger_type = db.Column(db.String(100), nullable=False) # e.g., 'shopify_new_product', 'schedule_daily'
    # إعدادات المحفز (مثلاً، في أي ساعة يتم التشغيل اليومي)
    trigger_config = db.Column(db.JSON)
    
    workflow = db.relationship('Workflow', back_populates='trigger')

class Action(db.Model):
    __tablename__ = 'actions'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    
    step_order = db.Column(db.Integer, nullable=False) # ترتيب تنفيذ الإجراء (1, 2, 3...)
    action_type = db.Column(db.String(100), nullable=False) # e.g., 'generate_text', 'send_whatsapp'
    # إعدادات الإجراء (مثلاً، الـ Prompt المستخدم أو رقم الواتساب)
    action_config = db.Column(db.JSON)
    
    workflow = db.relationship('Workflow', back_populates='actions')