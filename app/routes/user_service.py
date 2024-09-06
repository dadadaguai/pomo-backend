from http.client import responses

import pytz
from flask import Blueprint, jsonify, request, make_response
from app.models.User import User
from app.models.PomodoroSession import PomodoroSession
from app.models.PomodoroSummary import PomodoroSummary
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity


bp = Blueprint('api/user_service', __name__, url_prefix='/api/user_service')

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

    hashed_password = generate_password_hash(password) # 对密码进行hash操作。
    new_user = User(username=username, password_hash=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        user.last_login = datetime.utcnow()
        db.session.commit()

        # 创建 JWT
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        response = make_response(jsonify({
            'message': '登录成功',
            'user_id': user.id,
            'access_token': access_token
        }), 200)
        # 设置 HTTPOnly cookies
        response.set_cookie('user_id', str(user.id))
        response.set_cookie('access_token', access_token)
        return response
    else:
        return jsonify({'message': '用户名或密码错误'}), 401

# 以下暂未实现。

# 这段代码定义了一个受保护的路由 /protected，只有持有有效 JWT 的用户才能访问。如果用户验证通过，它将返回用户的 ID。
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'logged_in_as': current_user_id}), 200

# 在这里可以添加更多的 API 路由...
