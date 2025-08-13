import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 添加Flask超时配置
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30分钟
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB文件上传限制
    
    # 添加更多连接稳定性配置
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    mysql.init_app(app)
    CORS(app)

    # 注册蓝图
    from routes.test_case import test_case_bp
    from routes.project import project_bp
    from routes.upload import upload_bp
    from routes.ai_generate import ai_generate_bp
    from routes.logs import logs_bp
    app.register_blueprint(test_case_bp, url_prefix='/test_case')
    app.register_blueprint(project_bp, url_prefix='/project')
    app.register_blueprint(upload_bp)
    app.register_blueprint(ai_generate_bp, url_prefix='/ai_generate')
    app.register_blueprint(logs_bp, url_prefix='/logs')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app

if __name__ == '__main__':
    app = create_app()
    # 优化Flask运行配置
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        threaded=True,  # 启用多线程
        use_reloader=False  # 禁用自动重载，避免连接问题
    ) 