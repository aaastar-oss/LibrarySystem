import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from services.admin_service import add_book, delete_book, model_book, query_book, get_all_books
from services.user_service import  query_books, borrow_book, return_book, get_user_borrowed

# 初始化数据库连接
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

# 初始化服务对象
def init_services():
    db_connection = init_database()
    if db_connection is None:
        return None, None
    admin_service = admin_service(db_connection)
    user_service = user_service(db_connection)
    return admin_service, user_service

# 调用初始化函数
admin_service, user_service = init_services()
