from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models.db import execute_query
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
def get_projects():
    """获取所有项目列表"""
    try:
        logger.info("开始获取项目列表")
        projects = execute_query("SELECT id, name, description, maintainers FROM projects ORDER BY id ASC")
        logger.info(f"成功获取 {len(projects)} 个项目")
        return jsonify({'projects': projects})
    except Exception as e:
        error_msg = str(e)
        logger.error(f"获取项目列表失败: {error_msg}")
        
        # 根据错误类型返回不同的响应
        if "MySQL连接池未初始化" in error_msg:
            return jsonify({
                'error': '数据库连接未就绪，请稍后重试',
                'error_type': 'database_not_ready',
                'projects': []  # 返回空列表以保持前端兼容性
            }), 503  # 服务不可用
        elif "Lost connection" in error_msg or "Connection" in error_msg:
            return jsonify({
                'error': '数据库连接失败，请检查网络连接',
                'error_type': 'database_connection_failed',
                'projects': []
            }), 503
        else:
            return jsonify({
                'error': f'获取项目列表失败: {error_msg}',
                'error_type': 'unknown_error',
                'projects': []
            }), 500

@project_bp.route('/', methods=['POST'])
def create_project():
    """创建新项目"""
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        maintainers = data.get('maintainers', '')  # 获取维护人员信息
        
        if not name:
            return jsonify({'error': '项目名称不能为空'}), 400
        
        project_id = execute_query(
            "INSERT INTO projects (name, description, maintainers) VALUES (%s, %s, %s)",
            (name, description, maintainers),
            fetch=False
        )
        
        return jsonify({
            'id': project_id, 
            'name': name, 
            'description': description,
            'maintainers': maintainers
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目信息"""
    try:
        logger.info(f"开始更新项目 {project_id}")
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        maintainers = data.get('maintainers', '')  # 获取维护人员信息
        
        if not name:
            return jsonify({'error': '项目名称不能为空'}), 400
        
        affected_rows = execute_query(
            "UPDATE projects SET name=%s, description=%s, maintainers=%s WHERE id=%s",
            (name, description, maintainers, project_id),
            fetch=False
        )
        
        if affected_rows == 0:
            logger.warning(f"项目 {project_id} 不存在")
            return jsonify({'error': '项目不存在'}), 404
        
        logger.info(f"成功更新项目 {project_id}")
        return jsonify({
            'id': project_id, 
            'name': name, 
            'description': description,
            'maintainers': maintainers
        })
    except Exception as e:
        logger.error(f"更新项目 {project_id} 失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    try:
        logger.info(f"开始删除项目 {project_id}")
        
        # 先删除项目关联的测试用例关系
        execute_query("DELETE FROM project_cases WHERE project_id=%s", (project_id,), fetch=False)
        
        # 再删除项目本身
        affected_rows = execute_query("DELETE FROM projects WHERE id=%s", (project_id,), fetch=False)
        
        if affected_rows == 0:
            logger.warning(f"项目 {project_id} 不存在")
            return jsonify({'error': '项目不存在'}), 404
        
        logger.info(f"成功删除项目 {project_id}")
        return jsonify({'message': '项目删除成功'})
    except Exception as e:
        logger.error(f"删除项目 {project_id} 失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>/testcases', methods=['GET'])
def get_project_testcases(project_id):
    """获取项目关联的测试用例"""
    try:
        logger.info(f"开始获取项目 {project_id} 的测试用例")
        testcases = execute_query("""
            SELECT tc.id, tc.case_id, tc.title, tc.description, tc.preconditions, 
                   tc.steps, tc.expected_results, tc.priority, tc.category, tc.status
            FROM test_cases tc
            JOIN project_cases pc ON tc.id = pc.test_case_id
            WHERE pc.project_id = %s
            order by pc.id
        """, (project_id,))
        logger.info(f"成功获取项目 {project_id} 的 {len(testcases)} 个测试用例")
        return jsonify({'testcases': testcases})
    except Exception as e:
        logger.error(f"获取项目 {project_id} 测试用例失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>/testcase', methods=['POST'])
def add_test_case(project_id):
    """添加测试用例到指定项目"""
    try:
        data = request.json
        
        # 验证必需字段
        required_fields = ['case_id', 'title', 'priority', 'category', 'status']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'字段 {field} 不能为空'}), 400
        
        # 验证优先级值
        valid_priorities = ['P0', 'P1', 'P2', 'P3']
        if data['priority'] not in valid_priorities:
            return jsonify({'error': '无效的优先级值'}), 400
        
        # 验证状态值 - 统一转换为小写进行比较
        valid_statuses = ['success', 'failed', 'blocked', 'skipped', 'pending', 'running', 'draft']
        received_status = data['status'].lower() if data['status'] else ''
        if received_status not in valid_statuses:
            return jsonify({'error': f'无效的状态值: {data["status"]}, 有效值: {valid_statuses}'}), 400
        
        # 验证分类值 - 添加时只允许功能测试
        valid_categories = ['功能测试']
        if data['category'] not in valid_categories:
            return jsonify({'error': f'无效的分类值: {data["category"]}, 添加用例时只允许选择: {valid_categories}'}), 400
        
        # 验证项目是否存在
        project = execute_query("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        # 检查同一项目内case_id是否重复
        existing_case = execute_query("""
            SELECT id FROM test_cases 
            WHERE project_id = %s AND case_id = %s
        """, (project_id, data['case_id']))
        
        if existing_case:
            return jsonify({'error': f'用例ID "{data["case_id"]}" 在当前项目中已存在'}), 400
        
        # 获取当前时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 1. 插入test_cases表 - 确保状态值统一为小写
        test_case_id = execute_query("""
            INSERT INTO test_cases (
                case_id, title, description, preconditions, steps, 
                expected_results, priority, category, status, 
                created_at, updated_at, created_by, last_updated_by, project_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['case_id'],
            data['title'],
            data.get('description', ''),
            data.get('preconditions', ''),
            data.get('steps', ''),
            data.get('expected_results', ''),
            data['priority'],
            data['category'],
            received_status,  # 使用转换后的小写状态值
            current_time,
            current_time,
            '用户',  # created_by
            '用户',  # last_updated_by
            project_id
        ), fetch=False)
        
        # 2. 插入project_cases表建立关联关系
        execute_query("""
            INSERT INTO project_cases (project_id, test_case_id) 
            VALUES (%s, %s)
        """, (project_id, test_case_id), fetch=False)
        
        logger.info(f"成功添加测试用例 {data['case_id']} 到项目 {project_id}")
        return jsonify({
            'message': '测试用例添加成功',
            'test_case_id': test_case_id,
            'case_id': data['case_id'],
            'title': data['title'],
            'project_id': project_id
        }), 201
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"添加测试用例到项目 {project_id} 失败: {error_msg}")
        return jsonify({
            'error': f'添加测试用例失败: {error_msg}',
            'project_id': project_id
        }), 500