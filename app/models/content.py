from app import db
import datetime

class GeneratedContent(db.Model):
    __tablename__ = 'generated_content'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    template_used = db.Column(db.String(100)) # نوع القالب المستخدم
    prompt_text = db.Column(db.Text) # النص المستخدم في الـ Prompt
    result_text = db.Column(db.Text, nullable=False) # المحتوى الذي تم إنشاؤه
    word_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User')

    def __repr__(self):
        return f'<GeneratedContent {self.id} by User {self.user_id}>'

class ImageHistory(db.Model):
    __tablename__ = 'image_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    prompt_text = db.Column(db.Text)
    image_url = db.Column(db.String(512), nullable=False) # رابط الصورة على التخزين السحابي
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User')

    def __repr__(self):
        return f'<ImageHistory {self.id} by User {self.user_id}>'