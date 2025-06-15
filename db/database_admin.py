# /db/database.py
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict
import sys
import os

# 加入根目录，方便导入config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

def get_connection():
    conn_config = {
        'host': config.DB_HOST,
        'user': config.DB_USER,
        'password': config.DB_PASSWORD,
        'database': config.DB_NAME,
        'charset': 'utf8mb4',
        # 'port': config.DB_PORT,  # 如果你后面加了端口号配置，可以解开这行
    }
    return mysql.connector.connect(**conn_config)


def insert_book(book: Dict) -> bool:
    sql = """
        INSERT INTO books (id, title, author, publisher, publish_date, price, total_copies, available_copies)
        VALUES (%s, %s, %s, %s, %s, %s, 3, 3)
    """
    params = (
        book['id'], book['title'], book['author'], book['publisher'],
        book['pub_date'], book['price']
    )
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Error as e:
        print(f"[ERROR] insert_book: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def book_exists(book_id: str) -> bool:
    sql = "SELECT COUNT(*) FROM books WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (book_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except Error as e:
        print(f"[ERROR] book_exists: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_book_by_id(book_id: str) -> bool:
    sql = "DELETE FROM books WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[ERROR] delete_book_by_id: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_book_fields(book_id: str, new_data: Dict) -> bool:
    if not new_data:
        return False
    # 动态构造更新SQL
    fields = []
    params = []
    for k, v in new_data.items():
        if k == 'title':
            # 根据需求，title不可修改
            continue
        fields.append(f"{k} = %s")
        params.append(v)
    if not fields:
        return False
    params.append(book_id)
    sql = f"UPDATE books SET {', '.join(fields)} WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[ERROR] update_book_fields: {e}")
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
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"[ERROR] find_book_by_id_or_title: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def find_user_borrow_records(username: str) -> List[Dict]:
    sql = """
        SELECT b.id, b.title, br.borrow_date, br.return_date
        FROM borrowrecords br
        JOIN books b ON br.book_id = b.id
        JOIN users u ON br.user_id = u.id
        WHERE u.username = %s AND br.return_date IS NULL
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (username,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"[ERROR] find_user_borrow_records: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_books_fullinfo() -> List[Dict]:
    sql = """
        SELECT id, title, author, publisher, publish_date, price,
               total_copies AS stock, total_copies - available_copies AS borrowed
        FROM books
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"[ERROR] get_all_books_fullinfo: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
