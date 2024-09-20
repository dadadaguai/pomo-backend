import pytz
from flask import Blueprint, jsonify, request

from app.models.Keyword import Keyword
from app.models.User import User
from app.models.PomodoroSession import PomodoroSession
from app.models.PomodoroSummary import PomodoroSummary
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.utils.getKeyWords import getKeyWords

bp = Blueprint('api/pomodoro_service', __name__, url_prefix='/api/pomodoro_service')


# 正常结束的番茄钟请求.包含番茄钟的信息和笔记的信息
@bp.route('/add_normal_pomodoro', methods=['POST'])
# @jwt_required()  # 应用JWT保护 暂时不适用JWT进行验证
def add_normal_pomodoro():
    data = request.get_json()
    print(data)
    user_id = data.get('UserID')  # 获取当前用户的ID
    start_time_str = data.get('StartTime')
    end_time_str = data.get('EndTime')
    duration = data.get('Duration')
    completed = data.get('Completed')  # 默认为False
    summary_text = data.get('SummaryText')
    # 验证用户是否存在
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    # 将时间字符串转换为 datetime 对象
    try:
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=pytz.utc)
        end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=pytz.utc)
    except ValueError:
        return jsonify({'message': '无效的时间格式'}), 400
    # 创建番茄钟会话
    pomodoro_session = PomodoroSession(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        duration=duration,
        completed=completed
    )

    pomodoro_session.set_break_duration()  # 计算休息时间
    db.session.add(pomodoro_session)

    # 提交数据库会话以生成PomodoroSession的id
    db.session.commit()
    keywords = getKeyWords(summary_text)
    # 创建番茄钟总结，现在可以使用生成的pomodoro_session.id
    pomodoro_summary = PomodoroSummary(
        session_id=pomodoro_session.id,
        summary_text=summary_text,
        keywords=keywords
    )
    pomodoro_summary.set_md5_hash()
    db.session.add(pomodoro_summary)
    # 提交数据库会话
    db.session.commit()

    # 处理笔记的关键字提取。
    pomodoro_summary_id = pomodoro_summary.id
    for keyword in keywords:
        db.session.add(Keyword(
            user_id=user_id,
            pomodoro_summary_id=pomodoro_summary_id,
            pomodoro_session_id=pomodoro_session.id,
            keyword=keyword,
        ))
    db.session.commit()

    return jsonify({
        'message': '番茄钟添加成功',
        'pomodoro_session_id': pomodoro_session.id,
        'pomodoro_summary_id': pomodoro_summary.id
    }), 201


# 没有笔记的请求
@bp.route('/add_pomodoro_without_summary', methods=['POST'])
def add_pomodoro_without_summary():
    data = request.get_json()
    user_id = data.get('UserID')
    start_time_str = data.get('StartTime')
    end_time_str = data.get('EndTime')
    duration = data.get('Duration')
    completed = data.get('Completed', False)  # 默认为False

    # 验证用户是否存在
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    # 将时间字符串转换为 datetime 对象
    try:
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=pytz.utc)
        end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=pytz.utc)
    except ValueError:
        return jsonify({'message': '无效的时间格式'}), 400

    break_duration = 0
    if completed:
        is_break_duration = (end_time - start_time) / 1000 - duration
        if is_break_duration > 0:
            break_duration = is_break_duration  # 记录番茄的预定时间和实际时间的差值。

    # 创建番茄钟会话
    pomodoro_session = PomodoroSession(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        duration=duration,
        break_duration=break_duration,
        completed=completed
    )
    db.session.add(pomodoro_session)

    # 提交数据库会话以生成PomodoroSession的id
    db.session.commit()

    return jsonify({
        'message': '番茄钟添加成功',
        'pomodoro_session_id': pomodoro_session.id
    }), 201
