from app import db
from datetime import datetime

# 针对词云功能
class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pomodoro_summary_id = db.Column(db.Integer, db.ForeignKey('pomodoro_summaries.id'), nullable=True)
    pomodoro_session_id = db.Column(db.Integer, db.ForeignKey('pomodoro_sessions.id'), nullable=True)
    keyword = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Keyword %r>' % self.keyword