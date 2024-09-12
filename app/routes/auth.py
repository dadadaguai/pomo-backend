import jwt
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, decode_token
from flask_jwt_extended.exceptions import JWTExtendedException

bp = Blueprint('/auth', __name__, url_prefix='/auth')

@bp.route('/user', methods=['POST'])
@jwt_required()
def get_user():
    token = request.json.get('token', None)
    if not token:
        return jsonify({"msg": "Token is missing"}), 401

    try:
        # 解码和验证 token
        decoded_token = decode_token(token)
        # 获取用户身份
        current_user = decoded_token['sub']
        return jsonify({"msg": "success", "user_id": current_user}), 200
    except JWTExtendedException as e:
        return jsonify({"msg": str(e)}), 401





