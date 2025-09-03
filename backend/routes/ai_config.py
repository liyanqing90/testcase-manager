from flask import Blueprint, request, jsonify
from services.ai_config_service import AIConfigService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
ai_config_bp = Blueprint('ai_config', __name__)

# 初始化AI配置服务
ai_config_service = AIConfigService()

@ai_config_bp.route('/ai_configs', methods=['GET'])
def get_ai_configs():
    """获取所有AI配置列表"""
    try:
        # 获取查询参数
        include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
        
        configs = ai_config_service.get_all_configs(include_sensitive=include_sensitive)
        
        return jsonify({
            'success': True,
            'data': configs,
            'message': '获取配置列表成功'
        })
        
    except Exception as e:
        logger.error(f"获取AI配置列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取配置列表失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config/<int:config_id>', methods=['GET'])
def get_ai_config_by_id(config_id):
    """根据ID获取AI配置详情"""
    try:
        config = ai_config_service.get_config_by_id(config_id)
        
        if config:
            # 转换字段名以匹配前端
            response_data = {
                'id': config.get('id'),
                'configName': config.get('config_name'),
                'modelType': config.get('model_type'),
                'apiKey': config.get('api_key'),
                'baseUrl': config.get('model_url'),
                'modelVersion': config.get('model_version'),
                'promptPrice': str(config.get('prompt_price_per_1k', '0.001')),
                'completionPrice': str(config.get('completion_price_per_1k', '0.002')),
                'isEnabled': bool(config.get('is_enabled', 0)),
                'createdAt': config.get('created_at'),
                'updatedAt': config.get('updated_at')
            }
            return jsonify({
                'success': True,
                'data': response_data,
                'message': '获取配置详情成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取AI配置详情失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取配置详情失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config', methods=['GET'])
def get_ai_config():
    """获取AI配置"""
    try:
        config = ai_config_service.get_enabled_config()
        
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
                'message': '未找到启用的配置信息'
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
            'config_name': data.get('configName'),
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
        result = ai_config_service.save_config(config_data)
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"保存AI配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'保存配置失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config/<int:config_id>', methods=['PUT'])
def update_ai_config(config_id):
    """更新AI配置"""
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据不能为空'
            }), 400
        
        # 转换前端字段名到后端字段名
        config_data = {
            'config_name': data.get('configName'),
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
        
        # 更新配置
        result = ai_config_service.update_config(config_id, config_data)
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"更新AI配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'更新配置失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config/<int:config_id>/toggle_enabled', methods=['PUT'])
def toggle_config_enabled(config_id):
    """切换配置启用状态"""
    try:
        data = request.json
        
        if not data or 'enabled' not in data:
            return jsonify({
                'success': False,
                'message': '缺少启用状态参数'
            }), 400
        
        enabled = bool(data['enabled'])
        
        # 切换启用状态
        result = ai_config_service.toggle_config_enabled(config_id, enabled)
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"切换配置启用状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'切换状态失败: {str(e)}'
        }), 500

@ai_config_bp.route('/ai_config/<int:config_id>/delete', methods=['DELETE'])
def delete_ai_config(config_id):
    """删除AI配置"""
    try:
        # 删除配置
        result = ai_config_service.delete_config(config_id)
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        logger.error(f"删除AI配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'删除配置失败: {str(e)}'
        }), 500 