from flask import Blueprint, jsonify, request
from app.models.pomodoro import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity

bp = Blueprint('login', __name__, url_prefix='/login')

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
        return jsonify({'message': '登录成功', 'user_id': user.id}), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401
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