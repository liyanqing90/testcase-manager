from dotenv import load_dotenv
import os

def load_env_variables():
    """
    加载环境变量
    返回: dict
        - QWEN_BASE_URL: 基础URL
        - QWEN_API_KEY: API密钥
        - QWEN_MODEL: 模型版本
        - OPENAI_API_KEY: OpenAI API密钥
    """
    # 加载.env文件
    load_dotenv()
    
    # 获取环境变量
    env_vars = {
        'QWEN_BASE_URL': os.getenv('QWEN_BASE_URL'),
        'QWEN_API_KEY': os.getenv('QWEN_API_KEY'),
        'QWEN_MODEL': os.getenv('QWEN_MODEL'),
        'OPENAI_API_KEY': os.getenv('QWEN_API_KEY')  # 使用相同的API密钥
    }
    
    # 检查是否所有必要的环境变量都已设置
    missing_vars = [key for key, value in env_vars.items() if value is None]
    if missing_vars:
        raise ValueError(f"缺少必要的环境变量: {', '.join(missing_vars)}")
    
    return env_vars