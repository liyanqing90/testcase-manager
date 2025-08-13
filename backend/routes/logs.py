from flask import Blueprint, jsonify, request, Response
import os
import time
import json
from datetime import datetime
import re

logs_bp = Blueprint('logs', __name__)

# 日志文件路径配置
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_test_cases', 'logs', 'ai_tester.log')

def parse_log_line(line):
    """解析单行日志"""
    try:
        # 匹配日志格式: 2025-08-12 16:10:46 - root - INFO - 日志内容
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - ([^-]+) - (\w+) - (.+)'
        match = re.match(pattern, line.strip())
        
        if match:
            timestamp, agent, level, message = match.groups()
            return {
                'timestamp': timestamp,
                'agent': agent.strip(),
                'level': level.strip(),
                'message': message.strip(),
                'raw': line.strip()
            }
        else:
            # 如果格式不匹配，返回原始行
            return {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'agent': 'unknown',
                'level': 'INFO',
                'message': line.strip(),
                'raw': line.strip()
            }
    except Exception as e:
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'agent': 'system',
            'level': 'ERROR',
            'message': f'日志解析错误: {str(e)}',
            'raw': line.strip()
        }

def get_log_statistics(logs):
    """统计日志信息"""
    stats = {
        'total': len(logs),
        'info': 0,
        'warning': 0,
        'error': 0,
        'debug': 0
    }
    
    for log in logs:
        level = log.get('level', '').upper()
        if level in stats:
            stats[level.lower()] += 1
    
    return stats

@logs_bp.route('/get_logs', methods=['GET'])
def get_logs():
    """获取日志内容"""
    try:
        # 检查文件是否存在
        if not os.path.exists(LOG_FILE_PATH):
            return jsonify({
                'success': False,
                'error': '日志文件不存在',
                'logs': [],
                'statistics': get_log_statistics([])
            }), 404
        
        # 获取查询参数
        level_filter = request.args.get('level', '').upper()
        keyword_filter = request.args.get('keyword', '').lower()
        start_time = request.args.get('start_time', '')
        end_time = request.args.get('end_time', '')
        
        # 读取日志文件 - 尝试GBK编码，如果失败则使用UTF-8
        try:
            with open(LOG_FILE_PATH, 'r', encoding='gbk', errors='ignore') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # 如果GBK解码失败，尝试UTF-8
            with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        
        # 解析日志行
        logs = []
        for line in lines:
            if line.strip():  # 跳过空行
                log_entry = parse_log_line(line)
                if log_entry:
                    # 应用筛选条件
                    should_include = True
                    
                    # 日志级别筛选
                    if level_filter and log_entry['level'].upper() != level_filter:
                        should_include = False
                    
                    # 关键词筛选
                    if keyword_filter and keyword_filter not in log_entry['message'].lower():
                        should_include = False
                    
                    # 时间范围筛选
                    if start_time or end_time:
                        try:
                            log_time = datetime.strptime(log_entry['timestamp'], '%Y-%m-%d %H:%M:%S')
                            
                            if start_time:
                                start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                                if log_time < start_dt:
                                    should_include = False
                            
                            if end_time:
                                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                                if log_time > end_dt:
                                    should_include = False
                        except:
                            pass  # 时间解析失败时跳过时间筛选
                    
                    if should_include:
                        logs.append(log_entry)
        
        # 获取统计信息
        statistics = get_log_statistics(logs)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'statistics': statistics,
            'total_lines': len(lines),
            'file_path': LOG_FILE_PATH,
            'filtered_count': len(logs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'读取日志文件失败: {str(e)}',
            'logs': [],
            'statistics': get_log_statistics([])
        }), 500

@logs_bp.route('/stream_logs', methods=['GET'])
def stream_logs():
    """实时流式读取日志文件"""
    def generate():
        try:
            if not os.path.exists(LOG_FILE_PATH):
                yield f"data: {json.dumps({'error': '日志文件不存在'})}\n\n"
                return
            
            # 获取当前文件大小
            current_size = os.path.getsize(LOG_FILE_PATH)
            last_position = current_size
            
            while True:
                try:
                    # 检查文件是否有变化
                    current_size = os.path.getsize(LOG_FILE_PATH)
                    
                    if current_size > last_position:
                        # 文件有新内容，读取新增部分
                        print(f"检测到文件变化: {current_size} > {last_position}, 新增 {current_size - last_position} 字节")
                        try:
                            with open(LOG_FILE_PATH, 'r', encoding='gbk', errors='ignore') as f:
                                f.seek(last_position)
                                new_lines = f.readlines()
                                
                                print(f"GBK编码读取到 {len(new_lines)} 行新内容")
                                # 处理新读取的行
                                for line in new_lines:
                                    if line.strip():
                                        log_entry = parse_log_line(line)
                                        if log_entry:
                                            print(f"发送日志: {log_entry['timestamp']} [{log_entry['level']}] {log_entry['message'][:50]}...")
                                            yield f"data: {json.dumps(log_entry, ensure_ascii=False)}\n\n"
                                            
                        except UnicodeDecodeError:
                            print("GBK解码失败，尝试UTF-8编码")
                            # 如果GBK解码失败，尝试UTF-8
                            with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                                f.seek(last_position)
                                new_lines = f.readlines()
                                
                                print(f"UTF-8编码读取到 {len(new_lines)} 行新内容")
                                # 处理新读取的行
                                for line in new_lines:
                                    if line.strip():
                                        log_entry = parse_log_line(line)
                                        if log_entry:
                                            print(f"发送日志: {log_entry['timestamp']} [{log_entry['level']}] {log_entry['message'][:50]}...")
                                            yield f"data: {json.dumps(log_entry, ensure_ascii=False)}\n\n"
                        
                        last_position = current_size
                    
                    # 发送心跳保持连接活跃
                    yield f"data: {json.dumps({'heartbeat': True, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})}\n\n"
                    
                    # 等待1秒后再次检查
                    time.sleep(1)
                    
                except Exception as e:
                    yield f"data: {json.dumps({'error': f'读取错误: {str(e)}'})}\n\n"
                    time.sleep(5)  # 出错后等待5秒再重试
                    
        except Exception as e:
            yield f"data: {json.dumps({'error': f'流式读取失败: {str(e)}'})}\n\n"
    
    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Cache-Control'
    return response

@logs_bp.route('/clear_logs', methods=['POST'])
def clear_logs():
    """清空日志文件"""
    try:
        if not os.path.exists(LOG_FILE_PATH):
            return jsonify({
                'success': False,
                'error': '日志文件不存在'
            }), 404
        
        # 清空文件内容 - 保持原有编码
        with open(LOG_FILE_PATH, 'w', encoding='gbk') as f:
            f.write('')
        
        return jsonify({
            'success': True,
            'message': '日志文件已清空'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'清空日志文件失败: {str(e)}'
        }), 500

@logs_bp.route('/log_info', methods=['GET'])
def get_log_info():
    """获取日志文件信息"""
    try:
        if not os.path.exists(LOG_FILE_PATH):
            return jsonify({
                'success': False,
                'error': '日志文件不存在'
            }), 404
        
        file_stat = os.stat(LOG_FILE_PATH)
        
        return jsonify({
            'success': True,
            'file_path': LOG_FILE_PATH,
            'file_size': file_stat.st_size,
            'last_modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
            'created_time': datetime.fromtimestamp(file_stat.st_ctime).isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取日志文件信息失败: {str(e)}'
        }), 500 