# 引入 os 模块，用于操作系统功能，如文件路径和环境变量
import os

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 定义 Config 类，用于存储 Flask 应用的配置
class Config:
    # 定义一个秘密密钥，用于 Flask 应用的会话管理等
    # 首先尝试从环境变量 SECRET_KEY 中获取，如果没有设置，则使用一个默认的字符串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # 定义数据库的连接字符串
    # 首先尝试从环境变量 DATABASE_URL 中获取，如果没有设置，则使用 SQLite 数据库，数据库文件位于当前文件的同级目录下
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.db')
    # 设置 SQLAlchemy 不追踪对象的修改，避免在每次修改时都触发数据库操作
    SQLALCHEMY_TRACK_MODIFICATIONS = False