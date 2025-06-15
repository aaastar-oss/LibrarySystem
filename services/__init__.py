import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# 导入服务函数
from services.admin_service import add_book, delete_book, modify_book, query_book, query_all_books
from services.user_service import query_books, borrow_book, return_book, get_user_borrowed,get_user_info

# 初始化数据库连接（可选是否共享）
def init_database():
    try:
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("数据库连接成功")
        return db_connection
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

# 这里只返回连接，不要“初始化服务对象”
db_connection = init_database()
