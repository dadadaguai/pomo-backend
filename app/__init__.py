# 引入 Flask 类，用于创建 Flask 应用
from flask import Flask
# 引入 SQLAlchemy 类，用于数据库操作
from flask_sqlalchemy import SQLAlchemy
# 引入 CORS 类，用于处理跨源资源共享
from flask_cors import CORS
# 从 config 模块导入配置类
from config import Config
from flask_jwt_extended import JWTManager
from datetime import timedelta

# 创建 SQLAlchemy 实例，将用于应用中所有的数据库操作
db = SQLAlchemy()


# 定义 create_app 函数，用于创建和配置 Flask 应用
def create_app():
    # 创建 Flask 应用实例，__name__ 是当前模块的名称
    app = Flask(__name__)

    # 从 Config 类中加载配置到 Flask 应用
    app.config.from_object(Config)
    # 添加jwt
    app.config['JWT_SECRET_KEY'] = 'dadadaguai'  # 更改为一个安全的密钥,在实际应用中使用一个安全的随机值
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # 在生产环境中使用
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # 设置访问令牌过期时间
    jwt = JWTManager(app)

    # 初始化 SQLAlchemy 实例，与 Flask 应用关联
    db.init_app(app)

    # 启用 CORS，允许跨源请求
    CORS(app, supports_credentials=True)

    # 从 app.routes 模块导入 api 蓝图
    from app.routes import index, login, user_service,pomodoro_service
    # 注册 api 蓝图到 Flask 应用
    app.register_blueprint(index.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(user_service.bp)
    app.register_blueprint(pomodoro_service.bp)
    # 进入应用上下文，确保所有数据库操作都在应用的上下文中执行
    with app.app_context():
        # 创建所有在模型中定义的表，如果它们还不存在的话
        db.create_all()

    # 返回配置好的 Flask 应用实例
    return app