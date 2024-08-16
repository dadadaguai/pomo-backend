# 引入 SQLAlchemy ORM 模块 db，用于定义数据模型
from app import db
# 引入 datetime 模块，用于处理日期和时间
from datetime import datetime
# 引入 JSON 类型，用于存储 JSON 格式的数据
# from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_json import MutableJson
from sqlalchemy import Date


# 定义 User 类，继承自 db.Model，表示用户数据模型
class User(db.Model):
    # 指定数据库表名
    __tablename__ = 'users'

    # 定义列和数据类型，以及一些列的属性
    id = db.Column(db.Integer, primary_key=True)  # 定义一个整型列，设为主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 定义一个字符串列，长度为80，唯一且不允许为空
    password = db.Column(db.String(255), nullable=False)  # 定义一个字符串列，长度为255，不允许为空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 定义一个字符串列，长度为120，唯一且不允许为空
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 定义一个日期时间列，不允许为空，默认值为当前 UTC 时间
    last_login = db.Column(db.DateTime)  # 定义一个日期时间列，可为空

    # 通常在模型类中还可以定义一些方法，例如创建、读取、更新、删除等操作


# 定义 PomodoroSession 类，继承自 db.Model，表示番茄工作法会话的数据模型
class PomodoroSession(db.Model):
    # 指定数据库表名
    __tablename__ = 'pomodoro_sessions'

    # 定义列和数据类型，以及一些列的属性
    id = db.Column(db.Integer, primary_key=True)  # 定义一个整型列，设为主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 定义一个整型列，作为外键指向 users 表的 id 列，不允许为空
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 定义一个日期时间列，不允许为空，默认值为当前 UTC 时间
    end_time = db.Column(db.DateTime)  # 定义一个日期时间列，表示会话结束时间，可为空
    duration = db.Column(db.Integer)  # 定义一个整型列，表示会话持续时间（秒）
    break_duration = db.Column(db.Integer)  # 定义一个整型列，表示休息时间（秒）
    task_description = db.Column(db.Text)  # 定义一个文本列，表示任务描述
    completed = db.Column(db.Boolean, default=False)  # 定义一个布尔型列，表示会话是否完成，默认为 False

    # 通常在模型类中还可以定义一些方法，例如获取会话详情、更新状态等操作


# 定义 PomodoroSummary 模型，映射到 'pomodoro_summaries' 数据库表
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

    # 定义 Keyword 模型，映射到 'keywords' 数据库表
class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)  # 唯一标识符，主键
    primary_keyword = db.Column(db.String(50), nullable=False, unique=True)  # 主关键词，不允许为空且唯一
    related_keywords = db.Column(MutableJson, nullable=False, default=list)  # 相关的关键词列表，默认为空列表

# 定义 SummaryKeyword 模型，映射到 'summary_keywords' 数据库表，用于关联 PomodoroSummary 和 Keyword
class SummaryKeyword(db.Model):
    __tablename__ = 'summary_keywords'

    id = db.Column(db.Integer, primary_key=True)  # 唯一标识符，主键
    summary_id = db.Column(db.Integer, db.ForeignKey('pomodoro_summaries.id'),
                               nullable=False)  # 外键，关联到 pomodoro_summaries 表的 id
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'), nullable=False)  # 外键，关联到 keywords 表的 id


# 定义 DailyStatistic 类，继承自 db.Model，表示用户每天的番茄工作法统计数据模型
class DailyStatistic(db.Model):
    __tablename__ = 'daily_statistics'

    # 定义列和数据类型，以及一些列的属性
    id = db.Column(db.Integer, primary_key=True)  # 定义一个整型列，设为主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 定义一个整型列，作为外键指向 users 表的 id 列，不允许为空
    date = db.Column(Date, nullable=False)  # 定义一个日期列，存储统计的日期，不允许为空
    total_sessions = db.Column(db.Integer, default=0)  # 定义一个整型列，存储总的会话数，默认为0
    completed_sessions = db.Column(db.Integer, default=0)  # 定义一个整型列，存储完成的会话数，默认为0