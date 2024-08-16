# 引入 Flask Blueprint 类，用于创建 API 的蓝图
from flask import Blueprint, jsonify, request
# 从 app.models.pomodoro 模块导入所有定义的模型
from app.models.pomodoro import User, PomodoroSession, PomodoroSummary, Keyword, SummaryKeyword, DailyStatistic
# 从 app 模块导入 db 对象，它是 SQLAlchemy 的数据库实例
from app import db

# 创建一个名为 'api' 的蓝图，其视图函数将挂载在 '/api' 这个 URL 前缀下
bp = Blueprint('api', __name__, url_prefix='/api')

# 定义一个路由，当访问 '/api/users' 这个 URL 时，会调用 get_users 函数
@bp.route('/users', methods=['GET'])
def get_users():
    # 使用 User 模型查询所有用户记录
    users = User.query.all()
    # 将查询结果转换为字典列表，并使用 jsonify 将它们转换为 JSON 格式响应
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

# 定义一个路由，当访问 '/api/sessions' 这个 URL 时，会调用 get_sessions 函数
@bp.route('/sessions', methods=['GET'])
def get_sessions():
    # 使用 PomodoroSession 模型查询所有会话记录
    sessions = PomodoroSession.query.all()
    # 将查询结果转换为字典列表，注意 end_time 可能为 None，需要进行条件判断
    # 使用 jsonify 将它们转换为 JSON 格式响应
    return jsonify([{
        'id': session.id,
        'user_id': session.user_id,
        'start_time': session.start_time.isoformat(),  # 将日期时间格式化为 ISO 8601 字符串
        'end_time': session.end_time.isoformat() if session.end_time else None,  # 如果会话结束时间存在，则格式化，否则为 None
        'duration': session.duration,
        'break_duration': session.break_duration,
        'task_description': session.task_description,
        'completed': session.completed
    } for session in sessions])

# 添加更多路由... 这里可以继续添加其他路由来处理2不同的 API 端点