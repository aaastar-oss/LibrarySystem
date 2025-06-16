from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB

# 导入服务函数
from services.admin_service import add_book, delete_book, modify_book, query_book, query_all_books
from services.user_service import query_books, borrow_book, return_book, get_user_borrowed, get_user_info
from services.auth_service import authenticate, register

def init_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        print("MongoDB连接成功")
        return db
    except Exception as err:
        print(f"数据库连接失败: {err}")
        return None

# 这里只返回连接，不要“初始化服务对象”
db_connection = init_database()
