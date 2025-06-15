# /db/database_user.py
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4'
    )

def get_available_books() -> List[Dict]:
    sql = """
        SELECT id, title, author, publisher, publish_date, price, available_copies
        FROM books
        WHERE available_copies > 0
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"[ERROR] get_available_books: {e}")
        print(traceback.format_exc())
        return []
    finally:
        cursor.close()
        conn.close()

def get_user_borrowed_books(username: str) -> List[Dict]:
    sql = """
        SELECT b.id, b.title, br.borrow_date, br.due_date
        FROM borrowrecords br
        JOIN users u ON br.user_id = u.id
        JOIN books b ON br.book_id = b.id
        WHERE u.username = %s AND br.return_date IS NULL
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (username,))
        return cursor.fetchall()
    except Error as e:
        print(f"[ERROR] get_user_borrowed_books: {e}")
        print(traceback.format_exc())
        return []
    finally:
        cursor.close()
        conn.close()

def check_user_overdue(username: str) -> bool:
    sql = """
        SELECT COUNT(*)
        FROM borrowrecords br
        JOIN users u ON br.user_id = u.id
        WHERE u.username = %s AND br.return_date IS NULL AND br.due_date < NOW()
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (username,))
        count = cursor.fetchone()[0]
        return count > 0
    except Error as e:
        print(f"[ERROR] check_user_overdue: {e}")
        print(traceback.format_exc())
        return False
    finally:
        cursor.close()
        conn.close()

def insert_borrow_record(username: str, book_id: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return False
        user_id = user[0]

        cursor.execute("""
            INSERT INTO borrowrecords (user_id, book_id, borrow_date, due_date)
            VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY))
        """, (user_id, book_id))

        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = %s", (book_id,))

        conn.commit()
        return True
    except Error as e:
        print(f"[ERROR] insert_borrow_record: {e}")
        print(traceback.format_exc())
        return False
    finally:
        cursor.close()
        conn.close()

def return_book_record(username: str, book_id: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return False
        user_id = user[0]

        cursor.execute("""
            UPDATE borrowrecords
            SET return_date = NOW()
            WHERE user_id = %s AND book_id = %s AND return_date IS NULL
            LIMIT 1
        """, (user_id, book_id))

        if cursor.rowcount > 0:
            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = %s", (book_id,))
            conn.commit()
            return True
        else:
            return False
    except Error as e:
        print(f"[ERROR] return_book_record: {e}")
        print(traceback.format_exc())
        return False
    finally:
        cursor.close()
        conn.close()

def user_borrow_count(username: str) -> int:
    sql = """
        SELECT COUNT(*)
        FROM borrowrecords br
        JOIN users u ON br.user_id = u.id
        WHERE u.username = %s AND br.return_date IS NULL
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (username,))
        return cursor.fetchone()[0]
    except Error as e:
        print(f"[ERROR] user_borrow_count: {e}")
        print(traceback.format_exc())
        return 0
    finally:
        cursor.close()
        conn.close()

def book_exists(book_id: str) -> bool:
    sql = "SELECT COUNT(*) FROM books WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (book_id,))
        return cursor.fetchone()[0] > 0
    except Error as e:
        print(f"[ERROR] book_exists: {e}")
        print(traceback.format_exc())
        return False
    finally:
        cursor.close()
        conn.close()

def is_book_available(book_id: str) -> bool:
    sql = "SELECT available_copies FROM books WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (book_id,))
        result = cursor.fetchone()
        return result and result[0] > 0
    except Error as e:
        print(f"[ERROR] is_book_available: {e}")
        print(traceback.format_exc())
        return False
    finally:
        cursor.close()
        conn.close()

def find_book_by_id_or_title(keyword: str) -> Optional[Dict]:
    sql = """
        SELECT id, title, author, publisher, publish_date, price, total_copies, available_copies
        FROM books
        WHERE id = %s OR title LIKE %s
        LIMIT 1
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (keyword, f"%{keyword}%"))
        return cursor.fetchone()
    except Error as e:
        print(f"[ERROR] find_book_by_id_or_title: {e}")
        print(traceback.format_exc())
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    """
    根据用户名获取用户信息
    :param username: 用户名
    :return: 用户信息字典或None
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT username, role, phone, email, max_borrow
            FROM users 
            WHERE username = %s
        """, (username,))
        return cursor.fetchone()
    except Exception as e:
        print(f"数据库查询出错: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_borrowed_count(username):
    """
    获取用户当前借阅数量
    :param username: 用户名
    :return: 借阅数量
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM borrow_records 
            WHERE username = %s AND return_time IS NULL
        """, (username,))
        return cursor.fetchone()[0] or 0
    except Exception as e:
        print(f"获取借阅数量出错: {e}")
        return 0
    finally:
        if conn:
            conn.close()
