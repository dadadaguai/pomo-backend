# 从 app 模块导入 create_app 函数和 db 对象
from app import create_app, db
# 从 app.models.pomodoro 模块导入所有定义的模型
# from app.models.pomodoro import User, PomodoroSession, PomodoroSummary, Keyword, SummaryKeyword, DailyStatistic
from app.models.User import User
from app.models.PomodoroSession import PomodoroSession
from app.models.PomodoroSummary import PomodoroSummary
from app.models.Keyword import Keyword
from app.models.PomodoroCalendar import PomodoroCalendar
# 从 datetime 模块导入 datetime 和 timedelta
from datetime import datetime, timedelta


# 定义 init_db 函数，用于初始化数据库
def init_db():
    # 创建 Flask 应用实例
    app = create_app()
    # 进入应用上下文
    with app.app_context():
        # 删除所有现有的数据库表
        db.drop_all()

        # 创建所有表
        db.create_all()
        print("数据库初始化完成")


# 脚本入口点
if __name__ == "__main__":
    # 调用 init_db 函数初始化数据库
    init_db()