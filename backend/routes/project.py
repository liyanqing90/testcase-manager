from flask import Blueprint, request, jsonify
from backend.app import mysql

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
def get_projects():
    """获取所有项目列表"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, description, maintainers FROM projects")
        projects = cur.fetchall()
        cur.close()
        return jsonify({'projects': projects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO projects (name, description, maintainers) VALUES (%s, %s, %s)",
            (name, description, maintainers)
        )
        mysql.connection.commit()
        project_id = cur.lastrowid
        cur.close()
        
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
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        maintainers = data.get('maintainers', '')  # 获取维护人员信息
        
        if not name:
            return jsonify({'error': '项目名称不能为空'}), 400
        
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE projects SET name=%s, description=%s, maintainers=%s WHERE id=%s",
            (name, description, maintainers, project_id)
        )
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'error': '项目不存在'}), 404
        
        return jsonify({
            'id': project_id, 
            'name': name, 
            'description': description,
            'maintainers': maintainers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    try:
        cur = mysql.connection.cursor()
        
        # 先删除项目关联的测试用例关系
        cur.execute("DELETE FROM project_cases WHERE project_id=%s", (project_id,))
        
        # 再删除项目本身
        cur.execute("DELETE FROM projects WHERE id=%s", (project_id,))
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({'error': '项目不存在'}), 404
        
        return jsonify({'message': '项目删除成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>/testcases', methods=['GET'])
def get_project_testcases(project_id):
    """获取项目关联的测试用例"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT tc.id, tc.case_id, tc.title, tc.description, tc.preconditions, 
                   tc.steps, tc.expected_results, tc.priority, tc.category, tc.status
            FROM test_cases tc
            JOIN project_cases pc ON tc.id = pc.test_case_id
            WHERE pc.project_id = %s
        """, (project_id,))
        testcases = cur.fetchall()
        cur.close()
        return jsonify({'testcases': testcases})
    except Exception as e:
        return jsonify({'error': str(e)}), 500