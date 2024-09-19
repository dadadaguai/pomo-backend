from app.utils.configOperate import read_config, config_file, get_config
import os

def downloadDailyToPath(extracted_content, day):
    # 读取默认的配置文件
    path = get_config("daily_report")['generation_address']
    if not path:
        raise ValueError("日报保存路径未配置")
    print(path)
    # 定义文件名和完整路径
    filename = day + ".md"
    file_path = os.path.join(path, filename)

    # 确保目录存在，如果不存在则创建
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 检查文件是否存在，如果存在则删除
    if os.path.exists(file_path):
        os.remove(file_path)

    # 将内容写入.md文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(extracted_content)
    return 1

