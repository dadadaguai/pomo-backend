import pytz
from flask import Blueprint, jsonify, request
from app.models.User import User
from app.models.PomodoroSession import PomodoroSession
from app.models.PomodoroSummary import PomodoroSummary
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity


bp = Blueprint('api/index', __name__, url_prefix='/api/index')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'message': '所有字段都是必填的'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': '邮箱已被注册'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(data)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        user.last_login = datetime.utcnow()
        db.session.commit()

        # 创建 JWT
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify({
            'message': '登录成功',
            'user_name':user.username,
            'user_id': user.id,
            'access_token': access_token
        }), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401

# 以下暂未实现。


@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'logged_in_as': current_user_id}), 200

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

# 在这里可以添加更多的 API 路由...

# 正常结束的番茄钟请求
@bp.route('/add_normal_pomodoro', methods=['POST'])
def add_normal_pomodoro():
    data = request.get_json()
    user_id = data.get('UserID')
    start_time_str = data.get('StartTime')
    end_time_str = data.get('EndTime')
    duration = data.get('Duration')
    completed = data.get('Completed', False)  # 默认为False
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

    # 创建番茄钟总结，现在可以使用生成的pomodoro_session.id
    pomodoro_summary = PomodoroSummary(
        session_id=pomodoro_session.id,
        summary_text=summary_text
    )
    db.session.add(pomodoro_summary)

    # 提交数据库会话
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