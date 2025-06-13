# services/book_service.py
import datetime
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME  # 导入Mysql配置

class BookService:
    def __init__(self):
        self.db_config = {
            'host': DB_HOST,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME
        }
        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor(dictionary=True)

    def get_all_books(self):
        """获取所有图书"""
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        """根据ID获取图书"""
        self.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        return self.cursor.fetchone()

    def add_book(self, title, author, isbn, publication_date, available_copies):
        """添加新图书"""
        query = """
        INSERT INTO books (title, author, isbn, publication_date, available_copies, status)
        VALUES (%s, %s, %s, %s, %s, '可用')
        """
        self.cursor.execute(query, (title, author, isbn, publication_date, available_copies))
        self.connection.commit()
        return self.get_book_by_id(self.cursor.lastrowid)

    def update_book(self, book_id, title=None, author=None, isbn=None, publication_date=None, available_copies=None):
        """更新图书信息"""
        book = self.get_book_by_id(book_id)
        if not book:
            return None

        updates = []
        params = []

        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if author is not None:
            updates.append("author = %s")
            params.append(author)
        if isbn is not None:
            updates.append("isbn = %s")
            params.append(isbn)
        if publication_date is not None:
            updates.append("publication_date = %s")
            params.append(publication_date)
        if available_copies is not None:
            updates.append("available_copies = %s")
            params.append(available_copies)

        query = f"UPDATE books SET {', '.join(updates)} WHERE id = %s"
        params.append(book_id)

        self.cursor.execute(query, params)
        self.connection.commit()
        return self.get_book_by_id(book_id)

    def delete_book(self, book_id):
        """删除图书"""
        book = self.get_book_by_id(book_id)
        if not book:
            return False

        # 删除借阅记录
        self.cursor.execute("DELETE FROM borrowrecords WHERE book_id = %s", (book_id,))
        self.connection.commit()

        # 删除图书
        self.cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        self.connection.commit()
        return True

    def search_books(self, keyword):
        """根据关键词搜索图书"""
        query = """
        SELECT * FROM books WHERE title LIKE %s OR author LIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

    def query_books(self):
        """返回所有剩余副本>0的图书列表"""
        query = "SELECT id, title, author, available_copies FROM books WHERE available_copies > 0"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def borrow_book(self, user_id, book_id):
        """借阅图书"""
        book = self.get_book_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return False

        # 检查用户是否已经借阅了足够数量的书籍
        self.cursor.execute("""
        SELECT COUNT(*) FROM borrowrecords WHERE user_id = %s AND return_date IS NULL
        """, (user_id,))
        borrow_count = self.cursor.fetchone()['COUNT(*)']
        if borrow_count >= 5:
            return False

        borrow_date = datetime.datetime.now()
        due_date = borrow_date + datetime.timedelta(days=30)

        query = """
        INSERT INTO borrowrecords (user_id, book_id, borrow_date, due_date)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, book_id, borrow_date, due_date))
        self.connection.commit()

        # 更新图书的可用副本数和状态
        self.cursor.execute("""
        UPDATE books SET available_copies = available_copies - 1, status = '借出' WHERE id = %s
        """, (book_id,))
        self.connection.commit()
        return True

    def return_book(self, user_id, book_id):
        """归还图书"""
        book = self.get_book_by_id(book_id)
        if not book or book['status'] != '借出':
            return False

        # 更新借阅记录的归还日期
        self.cursor.execute("""
        UPDATE borrowrecords SET return_date = %s WHERE user_id = %s AND book_id = %s AND return_date IS NULL
        """, (datetime.datetime.now(), user_id, book_id))
        self.connection.commit()

        # 更新图书的可用副本数和状态
        self.cursor.execute("""
        UPDATE books SET available_copies = available_copies + 1, status = '可用' WHERE id = %s
        """, (book_id,))
        self.connection.commit()
        return True

    def get_user_borrowed(self, user_id):
        """返回指定用户借阅的图书信息列表"""
        query = """
        SELECT books.id, books.title, borrowrecords.due_date FROM books
        JOIN borrowrecords ON books.id = borrowrecords.book_id
        WHERE borrowrecords.user_id = %s AND borrowrecords.return_date IS NULL
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def __del__(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.connection.close()
