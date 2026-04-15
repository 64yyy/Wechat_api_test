import yaml
import os

def read_config():
    """读取 config/config.yaml 文件，返回字典"""
    # 获取当前文件所在目录的父目录，再拼接 config 文件夹
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)