from app import db
import datetime

class SEORepoort(db.Model):
    __tablename__ = 'seo_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    target_keyword = db.Column(db.String(255), nullable=False)
    # سيتم تخزين التقرير الكامل كـ JSON لسهولة التعامل معه وعرضه
    report_data = db.Column(db.JSON, nullable=False)
    # مثال على البيانات داخل الـ JSON:
    # {
    #   "seo_score": 85,
    #   "competitors": [{"url": "...", "word_count": 1500}, ...],
    #   "lsi_keywords": ["keyword1", "keyword2"],
    #   "recommendations": ["Increase word count", "Add keyword X to title"]
    # }
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User')

    def __repr__(self):
        return f'<SEORepoort for "{self.target_keyword}" by User {self.user_id}>'