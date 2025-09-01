from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app import mysql
from datetime import datetime

test_case_bp = Blueprint('test_case', __name__)
 
@test_case_bp.route('/', methods=['GET'])
def index():
    return {'msg': 'test_case blueprint works!'}

@test_case_bp.route('/check_duplicate', methods=['POST'])
def check_case_id_duplicate():
    """检查指定项目下是否存在某个case_id"""
    try:
        data = request.json
        project_id = data.get('project_id')
        case_id = data.get('case_id')
        
        if not project_id or not case_id:
            return jsonify({'error': '项目ID和用例ID不能为空'}), 400
        
        cur = mysql.connection.cursor()
        
        # 查询指定项目下是否存在该case_id
        cur.execute("""
            SELECT id 
            FROM test_cases 
            WHERE project_id = %s AND case_id = %s
        """, (project_id, case_id))
        
        result = cur.fetchone()
        cur.close()
        
        is_duplicate = result is not None
        
        return jsonify({
            'is_duplicate': is_duplicate,
            'project_id': project_id,
            'case_id': case_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@test_case_bp.route('/<int:test_case_id>/status', methods=['PUT'])
def update_test_case_status(test_case_id):
    """更新测试用例状态"""
    try:
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({'error': '状态参数不能为空'}), 400
        
        # 验证状态值 - 统一转换为小写进行比较
        valid_statuses = ['success', 'failed', 'blocked', 'skipped', 'pending', 'running', 'draft']
        received_status = status.lower() if status else ''
        if received_status not in valid_statuses:
            return jsonify({'error': f'无效的状态值: {status}, 有效值: {valid_statuses}'}), 400
        
        cur = mysql.connection.cursor()
        
        # 更新测试用例状态 - 确保状态值统一为小写
        cur.execute(
            "UPDATE test_cases SET status = %s, updated_at = %s, last_updated_by = %s WHERE id = %s",
            (received_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '用户', test_case_id)
        )
        
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'error': '测试用例不存在'}), 404
        
        return jsonify({
            'message': '状态更新成功',
            'test_case_id': test_case_id,
            'status': status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@test_case_bp.route('/<int:test_case_id>', methods=['DELETE'])
def delete_test_case(test_case_id):
    """删除测试用例"""
    try:
        cur = mysql.connection.cursor()
        
        # 1. 先查询测试用例信息，获取project_id
        cur.execute("""
            SELECT id, case_id, project_id, title 
            FROM test_cases 
            WHERE id = %s
        """, (test_case_id,))
        
        test_case = cur.fetchone()
        if not test_case:
            cur.close()
            return jsonify({'error': '测试用例不存在'}), 404
        
        # 正确访问查询结果字段（字典格式）
        case_id = test_case['case_id']
        project_id = test_case['project_id']
        title = test_case['title']
        
        # 检查project_id是否为空
        if project_id is None:
            cur.close()
            return jsonify({'error': '测试用例缺少项目ID信息'}), 400
        
        # 2. 删除project_cases表中的关联记录
        cur.execute("""
            DELETE FROM project_cases 
            WHERE project_id = %s AND test_case_id = %s
        """, (project_id, test_case_id))
        
        project_cases_deleted = cur.rowcount
        
        # 3. 删除test_cases表中的测试用例记录
        cur.execute("""
            DELETE FROM test_cases 
            WHERE id = %s
        """, (test_case_id,))
        
        test_cases_deleted = cur.rowcount
        
        # 提交事务
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'message': '测试用例删除成功',
            'deleted_case_id': case_id,
            'deleted_title': title,
            'project_id': project_id,
            'project_cases_deleted': project_cases_deleted,
            'test_cases_deleted': test_cases_deleted
        })
        
    except Exception as e:
        # 回滚事务
        try:
            mysql.connection.rollback()
        except:
            pass
        
        # 返回错误信息
        error_msg = str(e)
        return jsonify({
            'error': f'删除测试用例失败: {error_msg}',
            'test_case_id': test_case_id
        }), 500

@test_case_bp.route('/<int:test_case_id>', methods=['PUT'])
def update_test_case(test_case_id):
    """更新测试用例"""
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
        
        # 验证分类值 - 编辑时允许任何分类值，不进行限制
        # 注释掉分类值校验，允许保存原有的任何分类值
        # valid_categories = ['功能测试', '接口测试', 'UI自动化测试']
        # if data['category'] not in valid_categories:
        #     return jsonify({'error': f'无效的分类值: {data["category"]}, 有效值: {valid_categories}'}), 400
        
        cur = mysql.connection.cursor()
        
        # 检查同一项目内case_id是否重复（排除当前用例）
        cur.execute("""
            SELECT id FROM test_cases 
            WHERE project_id = %s AND case_id = %s AND id != %s
        """, (data['project_id'], data['case_id'], test_case_id))
        
        if cur.fetchone():
            cur.close()
            return jsonify({'error': f'用例ID "{data["case_id"]}" 在当前项目中已存在'}), 400
        
        # 获取当前时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 更新测试用例 - 确保状态值统一为小写
        cur.execute("""
            UPDATE test_cases SET 
                case_id = %s, title = %s, description = %s, preconditions = %s,
                steps = %s, expected_results = %s, priority = %s, category = %s,
                status = %s, updated_at = %s, last_updated_by = %s
            WHERE id = %s
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
            '用户',  # last_updated_by
            test_case_id
        ))
        
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'error': '测试用例不存在'}), 404
        
        return jsonify({
            'message': '测试用例更新成功',
            'test_case_id': test_case_id,
            'case_id': data['case_id'],
            'title': data['title']
        })
        
    except Exception as e:
        return jsonify({'error': f'更新测试用例失败: {str(e)}'}), 500 