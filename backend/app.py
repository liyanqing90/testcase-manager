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
    mysql.init_app(app)
    CORS(app)

    # 注册蓝图
    from routes.test_case import test_case_bp
    from routes.project import project_bp
    from routes.upload import upload_bp
    app.register_blueprint(test_case_bp, url_prefix='/test_case')
    app.register_blueprint(project_bp, url_prefix='/project')
    app.register_blueprint(upload_bp)

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True) 