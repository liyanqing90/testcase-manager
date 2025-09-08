# src/utils/ai_config_service.py
import mysql.connector
import logging
import time
from typing import Dict, Optional
import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
sys.path.insert(0, project_root)

# 先设置logger
logger = logging.getLogger(__name__)

# 导入配置
from config import Config
MYSQL_CONFIG = {
    'host': Config.MYSQL_HOST,
    'port': Config.MYSQL_PORT,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DB
}
logger.info(f"成功导入数据库配置: {Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}")

class AIConfigService:
    """AI配置服务，用于从数据库读取AI模型配置"""
    
    def __init__(self):
        self.config = MYSQL_CONFIG
        self._cached_config = None
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 缓存5分钟
    
    def get_ai_config(self, force_refresh: bool = False) -> Optional[Dict]:
        """
        获取AI配置信息
        
        Args:
            force_refresh: 是否强制刷新缓存
            
        Returns:
            AI配置字典，包含model_type, api_key, model_url, model_version等
        """
        try:
            # 检查缓存是否有效
            if not force_refresh and self._cached_config and self._is_cache_valid():
                logger.debug("使用缓存的AI配置")
                return self._cached_config
            
            # 从数据库读取配置
            config = self._load_from_database()
            if config:
                self._cached_config = config
                self._cache_timestamp = time.time()
                logger.info("成功从数据库加载AI配置")
                logger.info(f"配置详情 - 模型类型: {config.get('model_type', 'unknown')}, 模型版本: {config.get('model_version', 'unknown')}, 接口地址: {config.get('base_url', 'unknown')}")
                return config
            else:
                logger.warning("数据库中没有找到启用的AI配置")
                return None
                
        except Exception as e:
            logger.error(f"获取AI配置失败: {str(e)}")
            return None
    
    def _load_from_database(self) -> Optional[Dict]:
        """从数据库加载AI配置"""
        try:
            logger.info(f"尝试连接数据库: {self.config.get('host')}:{self.config.get('port', 3306)}/{self.config.get('database')}")
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            
            # 查询启用的AI配置
            query = """
                SELECT model_type, api_key, model_url, model_version, 
                       prompt_price_per_1k, completion_price_per_1k
                FROM ai_configs 
                WHERE is_enabled = 1
                ORDER BY updated_at DESC 
                LIMIT 1
            """
            logger.debug(f"执行SQL查询: {query}")
            cursor.execute(query)
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                logger.info(f"从数据库获取到配置: {result}")
                return {
                    'model_type': result['model_type'],
                    'api_key': result['api_key'],
                    'base_url': result['model_url'],  # 映射到base_url
                    'model_version': result['model_version'],
                    'prompt_price': float(result['prompt_price_per_1k']) if result['prompt_price_per_1k'] else 0.0,
                    'completion_price': float(result['completion_price_per_1k']) if result['completion_price_per_1k'] else 0.0
                }
            else:
                logger.warning("数据库查询结果为空，没有找到AI配置记录")
                return None
            
        except mysql.connector.Error as e:
            logger.error(f"MySQL连接错误: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"从数据库加载AI配置失败: {str(e)}")
            return None
    
    def _is_cache_valid(self) -> bool:
        """检查缓存是否仍然有效"""
        return (time.time() - self._cache_timestamp) < self._cache_ttl
    
    def get_autogen_config(self) -> Optional[Dict]:
        """
        获取适用于AutoGen的配置格式
        
        Returns:
            AutoGen配置字典
        """
        config = self.get_ai_config()
        if not config:
            return None
        
        # 根据模型类型返回不同的配置格式
        model_type = config.get('model_type', 'qwen')
        
        if model_type == 'volcengine':
            # 字节跳动（火山引擎）配置
            # AutoGen会自动在base_url后面添加/chat/completions，所以我们需要提供根URL
            base_url = config['base_url']
            if base_url.endswith('/chat/completions'):
                base_url = base_url.replace('/chat/completions', '')
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": base_url,
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'deepseek':
            # DeepSeek配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'zhipu':
            # 智谱AI配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'openai':
            # OpenAI配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'wenxin':
            # 百度文心一言配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'xunfei':
            # 讯飞星火配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'minimax':
            # MiniMax配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'moonshot':
            # 月之暗面配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == '360':
            # 360智脑配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'claude':
            # Claude (Anthropic)配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        elif model_type == 'gemini':
            # Gemini (Google)配置
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": config['base_url'],
                "price": [config['prompt_price'], config['completion_price']]
            }
        else:
            # 通义千问等默认配置
            # AutoGen会自动在base_url后面添加/chat/completions，所以我们需要提供根URL
            base_url = config['base_url']
            if base_url.endswith('/chat/completions'):
                base_url = base_url.replace('/chat/completions', '')
            return {
                "model": config['model_version'],
                "api_key": config['api_key'],
                "base_url": base_url,
                "price": [config['prompt_price'], config['completion_price']]
            }
    
    def get_langchain_config(self) -> Optional[Dict]:
        """
        获取适用于LangChain的配置格式
        
        Returns:
            LangChain配置字典
        """
        config = self.get_ai_config()
        if not config:
            return None
        
        # 根据模型类型返回不同的配置格式
        model_type = config.get('model_type', 'qwen')
        
        if model_type == 'volcengine':
            # 字节跳动（火山引擎）配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'deepseek':
            # DeepSeek配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'zhipu':
            # 智谱AI配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'openai':
            # OpenAI配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'wenxin':
            # 百度文心一言配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'xunfei':
            # 讯飞星火配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'minimax':
            # MiniMax配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'moonshot':
            # 月之暗面配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == '360':
            # 360智脑配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'claude':
            # Claude (Anthropic)配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        elif model_type == 'gemini':
            # Gemini (Google)配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
        else:
            # 通义千问等默认配置
            return {
                "base_url": config['base_url'],
                "api_key": config['api_key'],
                "model": config['model_version']
            }
    
    def check_database_connection(self) -> bool:
        """检查数据库连接是否正常"""
        try:
            logger.info(f"检查数据库连接: {self.config.get('host')}:{self.config.get('port', 3306)}/{self.config.get('database')}")
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SHOW TABLES LIKE 'ai_configs'")
            table_exists = cursor.fetchone() is not None
            
            cursor.close()
            conn.close()
            
            if table_exists:
                logger.info("数据库连接正常，ai_configs表存在")
                return True
            else:
                logger.error("ai_configs表不存在")
                return False
                
        except Exception as e:
            logger.error(f"数据库连接检查失败: {str(e)}")
            return False

# 全局实例
ai_config_service = AIConfigService() 