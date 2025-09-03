#!/usr/bin/env python3
"""
数据库连接测试脚本
"""
import mysql.connector
from mysql.connector import Error
from config import Config

def test_database_connection():
    """测试数据库连接"""
    try:
        print("正在测试数据库连接...")
        print(f"主机: {Config.MYSQL_HOST}")
        print(f"端口: {Config.MYSQL_PORT}")
        print(f"用户: {Config.MYSQL_USER}")
        print(f"数据库: {Config.MYSQL_DB}")
        
        # 创建连接
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            autocommit=True,
            use_unicode=True
        )
        
        if connection.is_connected():
            print("✅ 数据库连接成功!")
            
            # 测试查询
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL版本: {version['VERSION()']}")
            
            # 检查表是否存在
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"数据库中的表: {[table[f'Tables_in_{Config.MYSQL_DB}'] for table in tables]}")
            
            cursor.close()
            connection.close()
            print("✅ 数据库连接测试完成")
            return True
            
    except Error as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
