# services/admin_service.py
import mysql.connector
from config import DB_HOST,DB_USER,DB_PASSWORD,DB_NAME  #导入Mysql配置（如 DB_PATH = "library.db"）


def _get_db_connection():
    """获取数据库连接（内部工具函数）"""
    try:
       conn = mysql.connector.connect(host = DB_HOST,user = DB_USER,password = DB_PASSWORD,database = DB_NAME)
       return conn
    except mysql.connector.Error as e:
        print(f"[ERROE]数据库连接失败:{e}")
        return None
    


def add_book(book: dict) -> bool:
    """
    录入新图书
    :param book: 字典，包含 {"id": str, "title": str, "author": str, "publisher": str, "pub_date": str, "price": float}
    :return: 是否录入成功（True/False）
    """
    conn = _get_db_connection()
    try:
        # 检查图书编号是否已存在
        cursor = conn.cursor(dictionary = True)
        cursor.execute("SELECT id FROM books WHERE id=?", (book["id"],))
        if cursor.fetchone():
            return False  # 编号重复，录入失败

        # 插入新图书（库存初始1，已借出0）
        cursor.execute("""
            INSERT INTO books (id, title, author, publisher, pub_date, price)
            VALUES ("1", "《Python》", "李荣浩", "人民出版社","2085-5-4", "14")
        """, (book["id"], book["title"], book["author"], book["publisher"], book["pub_date"], book["price"]))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()  # 出错时回滚事务
        print(f"[ERROR]添加图书失败: {e}")
        return False
    finally:
        if conn:
            conn.close()


def delete_book(book_id: str) -> bool:
    """
    删除图书（需确保图书存在）
    :param book_id: 图书编号
    :return: 是否删除成功（True/False）
    """
    conn = _get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor(dictionary = True)
        # 检查图书是否存在
        cursor.execute("SELECT id FROM books WHERE id=%s", (book_id,))
        if not cursor.fetchone():
            return False  # 图书不存在，删除失败

        # 删除图书记录（级联删除借阅记录可选，示例简化为仅删图书）
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[ERROR]删除书籍失败: {e}")
        return False
    finally:
        if conn:
            conn.close()


def modify_book(book_id: str, new_data: dict) -> bool:
    """
    修改图书信息（仅修改传入的字段）
    :param book_id: 图书编号
    :param new_data: 字典，包含要修改的字段（如 {"author": "新作者", "price": 99.9}）
    :return: 是否修改成功（True/False）
    """
    conn = _get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor(dictionary = True)
        # 检查图书是否存在
        cursor.execute("SELECT id FROM books WHERE id=?", (book_id,))
        if not cursor.fetchone():
            return False  # 图书不存在，修改失败

        # 构造 SQL 更新语句和参数
        update_fields = []
        params = []
        for key, value in new_data.items():
            if key in ["author", "publisher", "pub_date", "price"]:  # 仅允许修改这些字段
                update_fields.append(f"{key}=?")
                params.append(value)
        params.append(book_id)  # WHERE 条件的参数

        if not update_fields:
            return True  # 无有效修改字段，直接返回成功

        update_sql = "UPDATE books SET " + ", ".join(update_fields) + " WHERE id=?"
        cursor.execute(update_sql, params)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"[ERROR]修改图书失败: {e}")
        return False
    finally:
        if conn:
            conn.close()


def query_book(keyword: str) -> tuple or None: # type: ignore
    """
    按图书编号/书名查询图书信息
    :param keyword: 图书编号（精确匹配）或书名（模糊匹配）
    :return: 图书信息元组 (id, title, author, publisher, pub_date, price, stock, borrowed) | None
    """
    conn = _get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary = True)
        # 精确匹配编号 + 模糊匹配书名
        cursor.execute("""
            SELECT id, title, author, publisher, pub_date, price, stock, borrowed 
            FROM books 
            WHERE id=%s OR title LIKE %s
        """, (keyword, f"%{keyword}%"))
        row = cursor.fetchone()
        if row:
            return (
                row["id"], row["title"], row["author"],
                row["publisher"], row["pub_date"], row["price"],
            )
        return None
    except mysql.connector.Error as e:
        print(f"[ERROR]查询图书失败: {e}")
        return None
    finally:
        if conn:
            conn.close()


def query_user(username: str) -> list:
    """
    查询用户的借阅记录
    :param username: 用户名
    :return: 借阅记录列表 [(book_id, title, borrow_date), ...]
    """
    conn = _get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # 关联查询借阅记录和图书信息
        cursor.execute("""
            SELECT b.id, b.title, br.borrow_date 
            FROM borrow_records br 
            JOIN books b ON br.book_id = b.id 
            WHERE br.username=?
        """, (username,))
        rows = cursor.fetchall()
        return [
            (row["id"], row["title"], row["borrow_date"]) 
            for row in rows
        ]
    except Exception as e:
        print(f"[ERROR] query_user 失败: {e}")      
        return None
    finally:
        if conn:
            conn.close()


def get_all_books() -> list:
    """
    获取所有图书的详细信息（含库存、已借出数）
    :return: 图书列表 [(id, title, author, publisher, pub_date, price, stock, borrowed), ...]
    """
    conn = _get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, author, publisher, pub_date, price 
            FROM books
        """)
        rows = cursor.fetchall()
        return [
            (
                row["id"], row["title"], row["author"],
                row["publisher"], row["pub_date"], row["price"],
            ) 
            for row in rows
        ]
    except Exception as e:                                  
        print(f"[ERROR] get_all_books 失败: {e}")     
        return None             
    finally:
        if conn:
            conn.close()
