import mysql.connector
from mysql.connector import Error, pooling
from config import Config

def get_db():
    """获取数据库连接"""
    # 延迟导入避免循环导入
    from backend.app import get_mysql_pool
    mysql_pool = get_mysql_pool()
    
    # 如果连接池为None，直接创建连接（解决Flask多进程问题）
    if mysql_pool is None:
        try:
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                charset='utf8mb4',
                autocommit=True,
                use_unicode=True,
                connection_timeout=3,
                auth_plugin='mysql_native_password'
            )
            return connection
        except Error as e:
            print(f"创建直接连接失败: {e}")
            raise Exception("MySQL连接池未初始化")
    
    try:
        connection = mysql_pool.get_connection()
        return connection
    except Error as e:
        print(f"获取数据库连接失败: {e}")
        raise e

def execute_query(query, params=None, fetch=True):
    """执行数据库查询"""
    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            
    except Error as e:
        if connection:
            connection.rollback()
        print(f"数据库查询失败: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def execute_many(query, params_list):
    """批量执行数据库操作"""
    connection = None
    cursor = None
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.executemany(query, params_list)
        connection.commit()
        return cursor.rowcount
    except Error as e:
        if connection:
            connection.rollback()
        print(f"批量数据库操作失败: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close() 