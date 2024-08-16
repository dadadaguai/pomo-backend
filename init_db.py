# 从 app 模块导入 create_app 函数和 db 对象
from app import create_app, db
# 从 app.models.pomodoro 模块导入所有定义的模型
from app.models.pomodoro import User, PomodoroSession, PomodoroSummary, Keyword, SummaryKeyword, DailyStatistic
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

        # 添加一些示例数据
        # 创建一个用户实例并添加到数据库会话
        user = User(username='testuser', password='testpass', email='test@example.com')
        db.session.add(user)

        # 创建一个番茄工作法会话实例并添加到数据库会话
        session = PomodoroSession(
            user_id=1,  # 假设用户 ID 为 1
            start_time=datetime.utcnow(),  # 会话开始时间为当前 UTC 时间
            end_time=datetime.utcnow() + timedelta(minutes=25),  # 会话结束时间为开始时间加 25 分钟
            duration=1500,  # 会话持续时间为 25 分钟，以秒为单位
            break_duration=300,  # 休息时间为 5 分钟，以秒为单位
            task_description="Implement database models",  # 任务描述
            completed=True  # 会话是否完成
        )
        db.session.add(session)

        # 创建番茄工作法会话总结实例并添加到数据库会话
        summary = PomodoroSummary(
            session_id=1,  # 假设会话 ID 为 1
            summary_text="Completed implementation of database models for the Pomodoro app.",
            char_count=len("Completed implementation of database models for the Pomodoro app."),  # 计算总结文本的字符数
            word_count=len("Completed implementation of database models for the Pomodoro app.".split())  # 计算总结文本的单词数
        )
        db.session.add(summary)

        # 创建关键词实例并添加到数据库会话
        keyword1 = Keyword(primary_keyword="database", related_keywords=["models", "SQL"])
        keyword2 = Keyword(primary_keyword="pomodoro", related_keywords=["time management", "productivity"])
        db.session.add(keyword1)
        db.session.add(keyword2)

        # 创建关键词与会话总结的关联实例并添加到数据库会话
        summary_keyword1 = SummaryKeyword(summary_id=1, keyword_id=1)
        summary_keyword2 = SummaryKeyword(summary_id=1, keyword_id=2)
        db.session.add(summary_keyword1)
        db.session.add(summary_keyword2)

        # 创建每日统计实例并添加到数据库会话
        daily_stat = DailyStatistic(
            user_id=1,  # 假设用户 ID 为 1
            date=datetime.utcnow().date(),  # 统计日期为当前 UTC 日期
            total_sessions=1,  # 总会话数为 1
            completed_sessions=1  # 完成的会话数为 1
        )
        db.session.add(daily_stat)

        # 提交数据库会话，保存所有添加的记录
        db.session.commit()

        # 打印初始化完成的消息
        print("Database initialized with sample data.")


# 脚本入口点
if __name__ == "__main__":
    # 调用 init_db 函数初始化数据库
    init_db()