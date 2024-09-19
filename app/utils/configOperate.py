import json
import os

# JSON配置文件路径
config_file = '../config/user.json'


# 读取配置文件
def read_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    else:
        return {}


# 写入配置文件
def write_config(config):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)


# 添加或修改配置
def set_config(key, value):
    config = read_config()
    config[key] = value
    write_config(config)
    print(f"Set {key} = {value}")


# 获取配置
def get_config(key):
    config = read_config()
    return config.get(key, None)


# 删除配置
def delete_config(key):
    config = read_config()
    if key in config:
        del config[key]
        write_config(config)
        print(f"Deleted {key}")
    else:
        print(f"{key} not found in configuration.")


# 示例使用
if __name__ == "__main__":
    # 设置新的配置项
    # set_config("daily_report", {"generation_address": "E:\\obsidian_not\\daily"})
    # 获取配置项
    print(get_config("daily_report"))