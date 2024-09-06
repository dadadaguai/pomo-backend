from app import db
from datetime import datetime
from sqlalchemy_json import MutableJson  # 导入 MutableJson

class PomodoroSummary(db.Model):
    __tablename__ = 'pomodoro_summaries'

    # 定义模型属性，对应数据库表的列
    id = db.Column(db.Integer, primary_key=True)  # 唯一标识符，主键
    session_id = db.Column(db.Integer, db.ForeignKey('pomodoro_sessions.id'),
                           nullable=False)  # 外键，关联到 pomodoro_sessions 表的 id
    summary_text = db.Column(db.Text)  # 会话的文本总结
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间，默认为当前 UTC 时间
    md5_hash = db.Column(db.String(32))  # 总结文本的 MD5 哈希值
    local_file_path = db.Column(db.String(255))  # 本地文件路径
    char_count = db.Column(db.Integer)  # 总结文本的字符数量
    word_count = db.Column(db.Integer)  # 总结文本的单词数量
    keywords = db.Column(MutableJson)  # 使用 MutableJson 存储列表
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 最后修改时间，默认为当前 UTC 时间，每次更新记录时自动设置

    def __init__(self, session_id, summary_text):
        self.session_id = session_id
        self.summary_text = summary_text
        self.md5_hash = self.calculate_md5_hash(summary_text)

    @staticmethod
    def calculate_md5_hash(text):
        import hashlib
        return hashlib.md5(text.encode('utf-8')).hexdigest()
