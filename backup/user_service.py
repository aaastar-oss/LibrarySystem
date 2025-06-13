# services/user_service.py
import mysql.connector
from config import DB_HOST,DB_USER,DB_PASSWORD,DB_NAME  #导入Mysql配置（如 DB_PATH = "library.db"）
from datetime import datetime, timedelta

#数据库连接

def _get_db_connection():
    """获取数据库连接（内部工具函数）"""
    try:
       conn = mysql.connector.connect(host = DB_HOST,user = DB_USER,password = DB_PASSWORD,database = DB_NAME)
       return conn
    except mysql.connector.Error as e:
        print(f"[ERROE]数据库连接失败:{e}")
        return None
'''
# 模拟图书数据库：图书ID -> [书名, 作者, 剩余副本数量]
_books = {
    "1001": ["Python编程", "张三", 3],
    "1002": ["数据结构", "李四", 2],
    "1003": ["操作系统", "王五", 1],
}
#新增用户数据存储
_users = {
    "zhangsan":"123456",
    "lisi":"1234567"
}
# 验证用户是否存在
def check_user(username:str)->bool:
    return username in _users


# 模拟用户借阅记录：用户名 -> {图书ID: 到期日期字符串}
_user_borrowed = {
    # "zhangsan": {"1001": "2025-06-20"},
}

from datetime import datetime, timedelta
'''

def query_books():
    """返回所有剩余副本>0的图书列表，格式 [(id, 书名, 作者, 剩余副本), ...]"""
    result = []
    conn = _get_db_connection()
    if conn is None:
        return result
    cursor = conn.cursor()
    cursor.execute("select * from books")
    rows = cursor.fetchall()
    for row in rows:
        result.append((row[0], row[1], row[2], row[3]))

    cursor.close()
    conn.close()
    return result

def borrow_book(user_id, book_id):
    # 获取数据库连接
    conn = get_database_connection()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        # 检查用户是否已经借阅了足够数量的书籍
        cursor.execute("SELECT COUNT(*) FROM borrowrecords WHERE UserID = %s AND ReturnDate IS NULL", (user_id,))
        borrow_count = cursor.fetchone()[0]
        if borrow_count >= 5:
            cursor.close()
            conn.close()
            return False

        # 检查图书是否可用
        cursor.execute("SELECT AvailableCopies FROM books WHERE BookID = %s", (book_id,))
        available_copies = cursor.fetchone()
        if not available_copies or available_copies[0] <= 0:
            cursor.close()
            conn.close()
            return False

        # 增加借阅记录
        due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        borrow_date = datetime.now().strftime("%Y-%m-%d")

        # 插入借阅记录
        cursor.execute("""
            INSERT INTO borrowrecords (UserID, BookID, BorrowDate, DueDate)
            VALUES (%s, %s, %s, %s)
        """, (user_id, book_id, borrow_date, due_date))

        # 更新书籍的可用数量
        cursor.execute("""
            UPDATE books
            SET AvailableCopies = AvailableCopies - 1, Status = '借出'
            WHERE BookID = %s
        """, (book_id,))

        # 提交事务
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as e:
        print(f"[ERROR] 数据库操作失败: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False


def return_book(username, book_id):
    """用户还书，成功返回True，否则False"""
    conn = _get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrowed_books WHERE username = %s AND book_id = %s", (username, book_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    # 还书成功，更新数据
    cursor.execute("DELETE FROM borrowed_books WHERE username = %s AND book_id = %s", (username, book_id))
    cursor.execute("UPDATE books SET remaining_copies = remaining_copies + 1 WHERE book_id = %s", (book_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_user_borrowed(username):
    """返回用户借阅的图书信息列表 [(id, 书名, 到期日期), ...]，没有则返回空列表"""
    result = []

    conn = _get_db_connection()
    if conn is None:
        return result

    cursor = conn.cursor()
    try:
        # 查询用户借阅的图书信息
        cursor.execute("""
            SELECT b.BookID, b.Title, br.DueDate
            FROM borrowrecords br
            JOIN books b ON br.BookID = b.BookID
            WHERE br.UserID = %s
        """, (username,))

        rows = cursor.fetchall()
        for row in rows:
            book_id, book_name, due_date = row
            result.append((book_id, book_name, due_date))

        conn.commit()
        cursor.close()
        conn.close()
        return result

    except mysql.connector.Error as e:
        print(f"[ERROR] 查询失败: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return []

