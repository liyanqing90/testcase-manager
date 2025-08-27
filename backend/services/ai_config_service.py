import mysql.connector
from mysql.connector import Error
from typing import Dict, Optional, List
import logging
from config import Config

logger = logging.getLogger(__name__)

class AIConfigService:
    def __init__(self):
        """初始化AI配置服务"""
        self.db_config = {
            'host': Config.MYSQL_HOST,
            'port': Config.MYSQL_PORT,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DB
        }
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def get_config(self) -> Optional[Dict]:
        """获取AI配置"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM ai_configs ORDER BY id ASC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return result
        except Error as e:
            logger.error(f"获取AI配置失败: {e}")
            return None
    
    def save_config(self, config_data: Dict) -> bool:
        """保存AI配置"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 检查是否已有配置
            check_query = "SELECT COUNT(*) FROM ai_configs"
            cursor.execute(check_query)
            count = cursor.fetchone()[0]
            
            if count > 0:
                # 更新现有配置
                update_query = """
                UPDATE ai_configs SET 
                    model_type = %s, 
                    api_key = %s, 
                    model_url = %s, 
                    model_version = %s,
                    prompt_price_per_1k = %s,
                    completion_price_per_1k = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
                """
                values = (
                    config_data.get('model_type'),
                    config_data.get('api_key'),
                    config_data.get('model_url'),
                    config_data.get('model_version'),
                    config_data.get('prompt_price_per_1k'),
                    config_data.get('completion_price_per_1k')
                )
            else:
                # 插入新配置
                insert_query = """
                INSERT INTO ai_configs 
                (model_type, api_key, model_url, model_version, prompt_price_per_1k, completion_price_per_1k)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    config_data.get('model_type'),
                    config_data.get('api_key'),
                    config_data.get('model_url'),
                    config_data.get('model_version'),
                    config_data.get('prompt_price_per_1k'),
                    config_data.get('completion_price_per_1k')
                )
                cursor.execute(insert_query, values)
            
            if count > 0:
                cursor.execute(update_query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info("AI配置保存成功")
            return True
            
        except Error as e:
            logger.error(f"保存AI配置失败: {e}")
            return False
    
    def validate_config(self, config_data: Dict) -> Dict[str, str]:
        """验证配置数据"""
        errors = {}
        
        if not config_data.get('model_type'):
            errors['model_type'] = '模型类型不能为空'
        
        if not config_data.get('api_key'):
            errors['api_key'] = 'API密钥不能为空'
        
        if not config_data.get('model_url'):
            errors['model_url'] = '模型URL不能为空'
        
        if not config_data.get('model_version'):
            errors['model_version'] = '模型版本不能为空'
        
        # 验证价格字段
        try:
            prompt_price = float(config_data.get('prompt_price_per_1k', 0))
            if prompt_price < 0:
                errors['prompt_price_per_1k'] = '输入价格不能为负数'
        except (ValueError, TypeError):
            errors['prompt_price_per_1k'] = '输入价格必须是有效数字'
        
        try:
            completion_price = float(config_data.get('completion_price_per_1k', 0))
            if completion_price < 0:
                errors['completion_price_per_1k'] = '输出价格不能为负数'
        except (ValueError, TypeError):
            errors['completion_price_per_1k'] = '输出价格必须是有效数字'
        
        return errors 