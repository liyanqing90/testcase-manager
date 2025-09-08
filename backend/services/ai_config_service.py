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
    
    def check_config_name_exists(self, config_name: str, exclude_id: int = None) -> bool:
        """检查配置名称是否已存在"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if exclude_id:
                query = "SELECT COUNT(*) FROM ai_configs WHERE config_name = %s AND id != %s"
                cursor.execute(query, (config_name, exclude_id))
            else:
                query = "SELECT COUNT(*) FROM ai_configs WHERE config_name = %s"
                cursor.execute(query, (config_name,))
            
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            
            return count > 0
        except Error as e:
            logger.error(f"检查配置名称失败: {e}")
            return False
    
    def get_all_configs(self, include_sensitive: bool = False) -> List[Dict]:
        """获取所有AI配置列表"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if include_sensitive:
                # 包含敏感字段的查询（用于编辑）
                query = """
                    SELECT id, config_name, model_type, api_key, model_url, model_version, 
                           prompt_price_per_1k, completion_price_per_1k, is_enabled,
                           created_at, updated_at
                    FROM ai_configs 
                    ORDER BY id ASC
                """
            else:
                # 不包含敏感字段的查询（用于列表显示）
                query = """
                    SELECT id, config_name, model_type, model_version, 
                           prompt_price_per_1k, completion_price_per_1k, is_enabled,
                           created_at, updated_at
                    FROM ai_configs 
                    ORDER BY id ASC
                """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # 确保is_enabled字段为整数类型
            for result in results:
                if 'is_enabled' in result:
                    result['is_enabled'] = int(result['is_enabled'])
            
            cursor.close()
            connection.close()
            
            return results
        except Error as e:
            logger.error(f"获取AI配置列表失败: {e}")
            return []
    
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

    def get_config_by_id(self, config_id: int) -> Optional[Dict]:
        """根据ID获取AI配置详情"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM ai_configs WHERE id = %s"
            cursor.execute(query, (config_id,))
            result = cursor.fetchone()
            
            # 确保is_enabled字段为整数类型
            if result and 'is_enabled' in result:
                result['is_enabled'] = int(result['is_enabled'])
            
            cursor.close()
            connection.close()
            
            return result
        except Error as e:
            logger.error(f"根据ID获取AI配置失败: {e}")
            return None
    
    def update_config(self, config_id: int, config_data: Dict) -> Dict:
        """更新AI配置，返回结果字典"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            config_name = config_data.get('config_name')
            if not config_name:
                return {'success': False, 'message': '配置名称不能为空'}
            
            # 检查配置名称是否已存在（排除当前配置）
            if self.check_config_name_exists(config_name, exclude_id=config_id):
                return {'success': False, 'message': f'配置名称"{config_name}"已存在，请通过列表编辑修改'}
            
            # 更新配置
            update_query = """
            UPDATE ai_configs SET 
                config_name = %s, 
                model_type = %s, 
                api_key = %s, 
                model_url = %s, 
                model_version = %s,
                prompt_price_per_1k = %s,
                completion_price_per_1k = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            values = (
                config_name,
                config_data.get('model_type'),
                config_data.get('api_key'),
                config_data.get('model_url'),
                config_data.get('model_version'),
                config_data.get('prompt_price_per_1k'),
                config_data.get('completion_price_per_1k'),
                config_id
            )
            
            cursor.execute(update_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"AI配置更新成功: {config_name}")
            return {'success': True, 'message': '配置更新成功'}
            
        except Error as e:
            logger.error(f"更新AI配置失败: {e}")
            return {'success': False, 'message': f'更新配置失败: {str(e)}'}
    
    def save_config(self, config_data: Dict) -> Dict:
        """保存AI配置，返回结果字典"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            config_name = config_data.get('config_name')
            if not config_name:
                return {'success': False, 'message': '配置名称不能为空'}
            
            # 检查配置名称是否已存在
            if self.check_config_name_exists(config_name):
                return {'success': False, 'message': f'配置名称"{config_name}"已存在，请通过列表编辑修改'}
            
            # 插入新配置
            insert_query = """
            INSERT INTO ai_configs 
            (config_name, model_type, api_key, model_url, model_version, prompt_price_per_1k, completion_price_per_1k)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                config_name,
                config_data.get('model_type'),
                config_data.get('api_key'),
                config_data.get('model_url'),
                config_data.get('model_version'),
                config_data.get('prompt_price_per_1k'),
                config_data.get('completion_price_per_1k')
            )
            
            cursor.execute(insert_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"AI配置保存成功: {config_name}")
            return {'success': True, 'message': '配置保存成功'}
            
        except Error as e:
            logger.error(f"保存AI配置失败: {e}")
            return {'success': False, 'message': f'保存配置失败: {str(e)}'}
    
    def validate_config(self, config_data: Dict) -> Dict[str, str]:
        """验证配置数据"""
        errors = {}
        
        if not config_data.get('config_name'):
            errors['config_name'] = '配置名称不能为空'
        
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
            errors['prompt_price_per_1k'] = '输入价格格式错误，请输入有效数字（如：0.001）'
        
        try:
            completion_price = float(config_data.get('completion_price_per_1k', 0))
            if completion_price < 0:
                errors['completion_price_per_1k'] = '输出价格不能为负数'
        except (ValueError, TypeError):
            errors['completion_price_per_1k'] = '输出价格格式错误，请输入有效数字（如：0.002）'
        
        return errors 

    def toggle_config_enabled(self, config_id: int, enabled: bool) -> Dict:
        """切换配置启用状态"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if enabled:
                # 如果要启用，先检查是否已有其他配置启用
                check_query = "SELECT COUNT(*) FROM ai_configs WHERE is_enabled = 1 AND id != %s"
                cursor.execute(check_query, (config_id,))
                enabled_count = cursor.fetchone()[0]
                
                if enabled_count > 0:
                    cursor.close()
                    connection.close()
                    return {'success': False, 'message': '已有其他配置处于启用状态，请先禁用后再启用此配置'}
                
                # 启用当前配置
                update_query = """
                UPDATE ai_configs SET 
                    is_enabled = 1
                WHERE id = %s
                """
                cursor.execute(update_query, (config_id,))
            else:
                # 如果要禁用，直接禁用当前配置
                update_query = """
                UPDATE ai_configs SET 
                    is_enabled = 0
                WHERE id = %s
                """
                cursor.execute(update_query, (config_id,))
            
            connection.commit()
            
            # 检查是否更新成功
            if cursor.rowcount == 0:
                cursor.close()
                connection.close()
                return {'success': False, 'message': '配置不存在'}
            
            cursor.close()
            connection.close()
            
            status_text = '启用' if enabled else '禁用'
            logger.info(f"AI配置状态切换成功: ID={config_id}, 状态={status_text}")
            return {'success': True, 'message': f'配置已{status_text}'}
            
        except Error as e:
            logger.error(f"切换配置启用状态失败: {e}")
            return {'success': False, 'message': f'切换状态失败: {str(e)}'}
    
    def get_enabled_config(self) -> Optional[Dict]:
        """获取当前启用的配置"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM ai_configs WHERE is_enabled = 1 ORDER BY updated_at DESC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            
            # 确保is_enabled字段为整数类型
            if result and 'is_enabled' in result:
                result['is_enabled'] = int(result['is_enabled'])
            
            cursor.close()
            connection.close()
            
            return result
        except Error as e:
            logger.error(f"获取启用配置失败: {e}")
            return None

    def delete_config(self, config_id: int) -> Dict:
        """删除AI配置"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 先获取配置信息用于日志记录
            select_query = "SELECT config_name FROM ai_configs WHERE id = %s"
            cursor.execute(select_query, (config_id,))
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                connection.close()
                return {'success': False, 'message': '配置不存在'}
            
            config_name = result[0]
            
            # 删除配置
            delete_query = "DELETE FROM ai_configs WHERE id = %s"
            cursor.execute(delete_query, (config_id,))
            connection.commit()
            
            # 检查是否删除成功
            if cursor.rowcount == 0:
                cursor.close()
                connection.close()
                return {'success': False, 'message': '删除失败，配置可能已被删除'}
            
            cursor.close()
            connection.close()
            
            logger.info(f"AI配置删除成功: ID={config_id}, 名称={config_name}")
            return {'success': True, 'message': f'配置"{config_name}"已删除'}
            
        except Error as e:
            logger.error(f"删除AI配置失败: {e}")
            return {'success': False, 'message': f'删除配置失败: {str(e)}'} 