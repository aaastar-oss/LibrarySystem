# services/book_service.py
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, MONGO_DB

class BookService:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.books = self.db.books
        self.borrowrecords = self.db.borrowrecords

    def get_all_books(self):
        """获取所有图书"""
        return list(self.books.find())

    def get_book_by_id(self, book_id):
        """根据ID获取图书"""
        try:
            return self.books.find_one({"_id": ObjectId(book_id)})
        except Exception:
            return None

    def add_book(self, title, author, isbn, publication_date, available_copies):
        """添加新图书"""
        doc = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "publication_date": publication_date,
            "available_copies": available_copies,
            "status": "可用"
        }
        result = self.books.insert_one(doc)
        return self.get_book_by_id(result.inserted_id)

    def update_book(self, book_id, title=None, author=None, isbn=None, publication_date=None, available_copies=None):
        """更新图书信息"""
        update = {}
        if title is not None:
            update["title"] = title
        if author is not None:
            update["author"] = author
        if isbn is not None:
            update["isbn"] = isbn
        if publication_date is not None:
            update["publication_date"] = publication_date
        if available_copies is not None:
            update["available_copies"] = available_copies
        if not update:
            return None
        result = self.books.update_one({"_id": ObjectId(book_id)}, {"$set": update})
        if result.matched_count == 0:
            return None
        return self.get_book_by_id(book_id)

    def delete_book(self, book_id):
        """删除图书"""
        try:
            _id = ObjectId(book_id)
        except Exception:
            return False
        self.borrowrecords.delete_many({"book_id": book_id})
        result = self.books.delete_one({"_id": _id})
        return result.deleted_count > 0

    def search_books(self, keyword):
        """根据关键词搜索图书"""
        return list(self.books.find({
            "$or": [
                {"title": {"$regex": keyword}},
                {"author": {"$regex": keyword}}
            ]
        }))

    def query_books(self):
        """返回所有剩余副本>0的图书列表"""
        return list(self.books.find({"available_copies": {"$gt": 0}}, {"title": 1, "author": 1, "available_copies": 1}))

    def borrow_book(self, user_id, book_id):
        """借阅图书"""
        book = self.get_book_by_id(book_id)
        if not book or book.get('available_copies', 0) <= 0:
            return False
        borrow_count = self.borrowrecords.count_documents({"user_id": user_id, "return_date": None})
        if borrow_count >= 5:
            return False
        borrow_date = datetime.datetime.now()
        due_date = borrow_date + datetime.timedelta(days=30)
        self.borrowrecords.insert_one({
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": borrow_date,
            "due_date": due_date,
            "return_date": None
        })
        self.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$inc": {"available_copies": -1}, "$set": {"status": "借出"}}
        )
        return True

    def return_book(self, user_id, book_id):
        """归还图书"""
        book = self.get_book_by_id(book_id)
        if not book or book.get('status') != '借出':
            return False
        result = self.borrowrecords.update_one(
            {"user_id": user_id, "book_id": book_id, "return_date": None},
            {"$set": {"return_date": datetime.datetime.now()}}
        )
        if result.modified_count == 0:
            return False
        self.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$inc": {"available_copies": 1}, "$set": {"status": "可用"}}
        )
        return True

    def get_user_borrowed(self, user_id):
        """返回指定用户借阅的图书信息列表"""
        records = list(self.borrowrecords.find({"user_id": user_id, "return_date": None}))
        result = []
        for rec in records:
            book = self.get_book_by_id(rec["book_id"])
            if book:
                result.append({
                    "id": str(book["_id"]),
                    "title": book.get("title"),
                    "due_date": rec.get("due_date")
                })
        return result

    def __del__(self):
        self.client.close()
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
