from flask import Blueprint, request, jsonify
from services.ai_config_service import AIConfigService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
ai_config_bp = Blueprint('ai_config', __name__)

# 初始化AI配置服务
ai_config_service = AIConfigService()

@ai_config_bp.route('/ai_config', methods=['GET'])
def get_ai_config():
    """获取AI配置"""
    try:
        config = ai_config_service.get_config()
        
        if config:
            # 转换字段名以匹配前端
            response_data = {
                'modelType': config.get('model_type'),
                'apiKey': config.get('api_key'),
                'baseUrl': config.get('model_url'),
                'modelVersion': config.get('model_version'),
                'promptPrice': str(config.get('prompt_price_per_1k', '0.001')),
                'completionPrice': str(config.get('completion_price_per_1k', '0.002'))
            }
            return jsonify({
                'success': True,
                'data': response_data,
                'message': '获取配置成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '未找到配置信息'
            }), 404
            
    except Exception as e:
        logger.error(f"获取AI配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取配置失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config', methods=['POST'])
def save_ai_config():
    """保存AI配置"""
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据不能为空'
            }), 400
        
        # 转换前端字段名到后端字段名
        config_data = {
            'model_type': data.get('modelType'),
            'api_key': data.get('apiKey'),
            'model_url': data.get('baseUrl'),
            'model_version': data.get('modelVersion'),
            'prompt_price_per_1k': data.get('promptPrice'),
            'completion_price_per_1k': data.get('completionPrice')
        }
        
        # 验证配置数据
        validation_errors = ai_config_service.validate_config(config_data)
        if validation_errors:
            return jsonify({
                'success': False,
                'message': '配置验证失败',
                'errors': validation_errors
            }), 400
        
        # 保存配置
        if ai_config_service.save_config(config_data):
            return jsonify({
                'success': True,
                'message': '配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置保存失败'
            }), 500
            
    except Exception as e:
        logger.error(f"保存AI配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'保存配置失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config', methods=['PUT'])
def update_ai_config():
    """更新AI配置（与POST方法相同）"""
    return save_ai_config() 