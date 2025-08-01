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
        
        # 验证状态值
        valid_statuses = ['success', 'failed', 'blocked', 'skipped', 'pending', 'running', 'draft']
        if status not in valid_statuses:
            return jsonify({'error': '无效的状态值'}), 400
        
        cur = mysql.connection.cursor()
        
        # 更新测试用例状态
        cur.execute(
            "UPDATE test_cases SET status = %s, updated_at = %s, last_updated_by = %s WHERE id = %s",
            (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '用户', test_case_id)
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