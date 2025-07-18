from app import db
import datetime

class MarketingPlan(db.Model):
    __tablename__ = 'marketing_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    project_name = db.Column(db.String(255))
    project_description_input = db.Column(db.Text)
    
    # الخطة الكاملة يتم تخزينها كـ JSON
    generated_plan_data = db.Column(db.JSON, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User')

    def __repr__(self):
        return f'<MarketingPlan for "{self.project_name}" by User {self.user_id}>'