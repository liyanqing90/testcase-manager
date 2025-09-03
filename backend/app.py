import sys
import os
import time
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MySQL连接池配置
mysql_pool = None

def get_mysql_pool():
    """获取MySQL连接池"""
    global mysql_pool
    return mysql_pool

def set_mysql_pool(pool):
    """设置MySQL连接池"""
    global mysql_pool
    mysql_pool = pool

def create_app():
    global mysql_pool
    start_time = time.time()
    logger.info("开始创建Flask应用...")
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 添加Flask超时配置
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30分钟
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB文件上传限制
    
    # 添加更多连接稳定性配置
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    logger.info("Flask应用配置完成")
    
    # 初始化MySQL连接池
    logger.info("开始初始化MySQL连接池...")
    db_start_time = time.time()
    try:
        mysql_pool = pooling.MySQLConnectionPool(
            pool_name="testcase_pool",
            pool_size=5,  # 适中的连接池大小
            pool_reset_session=False,  # 不重置会话，提高速度
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            autocommit=True,
            use_unicode=True,
            connection_timeout=3,  # 连接超时3秒
            auth_plugin='mysql_native_password',  # 指定认证插件
            connect_timeout=3,  # 连接超时
            read_timeout=30,  # 读取超时
            write_timeout=30,  # 写入超时
            raise_on_warnings=False,  # 不抛出警告
            sql_mode='',  # 禁用严格模式提高兼容性
            init_command="SET SESSION sql_mode=''"  # 初始化命令
        )
        db_init_time = time.time() - db_start_time
        logger.info(f"MySQL连接池初始化成功，耗时: {db_init_time:.2f}秒")
    except Exception as e:
        db_init_time = time.time() - db_start_time
        logger.error(f"MySQL连接池初始化失败，耗时: {db_init_time:.2f}秒，错误: {e}")
        mysql_pool = None
    
    logger.info("配置CORS...")
    CORS(app)

    # 注册蓝图
    logger.info("开始注册蓝图...")
    blueprint_start_time = time.time()
    
    from routes.test_case import test_case_bp
    from routes.project import project_bp
    from routes.upload import upload_bp
    from routes.ai_generate import ai_generate_bp
    from routes.logs import logs_bp
    from routes.ai_config import ai_config_bp
    
    app.register_blueprint(test_case_bp, url_prefix='/test_case')
    app.register_blueprint(project_bp, url_prefix='/project')
    app.register_blueprint(upload_bp)
    app.register_blueprint(ai_generate_bp, url_prefix='/ai_generate')
    app.register_blueprint(logs_bp, url_prefix='/logs')
    app.register_blueprint(ai_config_bp, url_prefix='/api')
    
    blueprint_time = time.time() - blueprint_start_time
    logger.info(f"蓝图注册完成，耗时: {blueprint_time:.2f}秒")

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    total_time = time.time() - start_time
    logger.info(f"Flask应用创建完成，总耗时: {total_time:.2f}秒")
    return app

if __name__ == '__main__':
    logger.info("启动Flask应用...")
    app = create_app()
    # 优化Flask运行配置
    logger.info("Flask应用启动完成，开始监听请求...")
    app.run(
        host='0.0.0.0', 
        port=8000, 
        debug=True,
        threaded=True,  # 启用多线程
        use_reloader=False  # 禁用自动重载，避免连接问题
    ) 