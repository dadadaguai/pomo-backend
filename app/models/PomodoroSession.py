from app import db
from datetime import datetime

class PomodoroSession(db.Model):
    __tablename__ = 'pomodoro_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    break_duration = db.Column(db.Integer, default=-1)  # 默认值为-1
    task_description = db.Column(db.Text) # 任务描述，暂时还用不上
    completed = db.Column(db.Boolean, default=False) # 番茄钟完成情况状态

    def __repr__(self):
        return '<PomodoroSession %r>' % self.id

    def set_break_duration(self, end_time, duration):
        self.end_time = end_time
        self.duration = duration
        if self.completed:
            # 计算休息时间，假设 end_time 和 start_time 都是以 datetime 对象存储的
            self.break_duration = (self.end_time - self.start_time).seconds / 1000 - self.duration


# 注意：在插入新记录之前，需要调用 set_end_time_and_duration 方法来设置 end_time 和 duration，并计算 break_duration。