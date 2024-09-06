from app import db
from datetime import datetime

# 一是为了前端的番茄日历的显示，二是方便以后的统计分析。每次登录验证通过后，就更新一下前一天的情况。然后在有一些按钮那里，可以更新当天的。到时候再看。

class PomodoroCalendar(db.Model):
    __tablename__ = 'pomodoro_calendar'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    valid_pomodoros = db.Column(db.Integer, default=0)  # 有效番茄钟的个数
    invalid_pomodoros = db.Column(db.Integer, default=0)  # 无效番茄钟的个数
    total_pomodoro_duration = db.Column(db.Integer, default=0)  # 番茄钟总时长（秒）
    total_break_duration = db.Column(db.Integer, default=0)  # 总休息时长（秒）

    def __repr__(self):
        return '<PomodoroCalendar %r>' % self.date