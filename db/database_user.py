# /db/database_user.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Dict, Optional
import sys
import os
import traceback
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def get_connection():
    client = MongoClient(config.MONGO_URI)
    db = client[config.MONGO_DB]
    return db

def get_available_books() -> List[Dict]:
    try:
        db = get_connection()
        books = db.books.find({"available_copies": {"$gt": 0}})
        return list(books)
    except Exception as e:
        print(f"[ERROR] get_available_books: {e}")
        print(traceback.format_exc())
        return []

def get_user_borrowed_books(username: str) -> List[Dict]:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return []
        now = datetime.datetime.now()
        records = db.borrowrecords.find({"user_id": str(user["_id"]), "return_date": None})
        result = []
        for rec in records:
            book = db.books.find_one({"id": int(rec["book_id"])})
            if book:
                borrow_date = rec.get("borrow_date")
                due_date = rec.get("due_date")
                # 正确判断是否超期
                status = "normal"
                if isinstance(due_date, datetime.datetime) and now > due_date:
                    status = "overdue"
                borrow_date_str = borrow_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(borrow_date, datetime.datetime) else str(borrow_date)
                due_date_str = due_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(due_date, datetime.datetime) else str(due_date)
                result.append({
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "author": book.get("author"),
                    "borrow_date": borrow_date_str,
                    "due_date": due_date_str,
                    "status": status
                })
        return result
    except Exception as e:
        print(f"[ERROR] get_user_borrowed_books: {e}")
        print(traceback.format_exc())
        return []

def check_user_overdue(username: str) -> bool:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return False
        count = db.borrowrecords.count_documents({
            "user_id": str(user["_id"]),
            "return_date": None,
            "due_date": {"$lt": datetime.datetime.now()}
        })
        return count > 0
    except Exception as e:
        print(f"[ERROR] check_user_overdue: {e}")
        print(traceback.format_exc())
        return False

def insert_borrow_record(username: str, book_id: str) -> bool:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return False
        book = db.books.find_one({"id": int(book_id)})
        if not book or book.get("available_copies", 0) <= 0:
            return False
        db.borrowrecords.insert_one({
            "user_id": str(user["_id"]),
            "book_id": str(book_id),
            "borrow_date": datetime.datetime.now(),
            "due_date": datetime.datetime.now() + datetime.timedelta(days=30),
            "return_date": None
        })
        db.books.update_one({"id": int(book_id)}, {"$inc": {"available_copies": -1}})
        return True
    except Exception as e:
        print(f"[ERROR] insert_borrow_record: {e}")
        print(traceback.format_exc())
        return False

def return_book_record(username: str, book_id: str) -> bool:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return False
        result = db.borrowrecords.update_one(
            {"user_id": str(user["_id"]), "book_id": str(book_id), "return_date": None},
            {"$set": {"return_date": datetime.datetime.now()}}
        )
        if result.modified_count > 0:
            db.books.update_one({"id": int(book_id)}, {"$inc": {"available_copies": 1}})
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] return_book_record: {e}")
        print(traceback.format_exc())
        return False

def user_borrow_count(username: str) -> int:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return 0
        count = db.borrowrecords.count_documents({"user_id": str(user["_id"]), "return_date": None})
        return count
    except Exception as e:
        print(f"[ERROR] user_borrow_count: {e}")
        print(traceback.format_exc())
        return 0

def book_exists(book_id: str) -> bool:
    try:
        db = get_connection()
        return db.books.count_documents({"id": int(book_id)}) > 0
    except Exception as e:
        print(f"[ERROR] book_exists: {e}")
        print(traceback.format_exc())
        return False

def is_book_available(book_id: str) -> bool:
    try:
        db = get_connection()
        book = db.books.find_one({"id": int(book_id)})
        return book and book.get("available_copies", 0) > 0
    except Exception as e:
        print(f"[ERROR] is_book_available: {e}")
        print(traceback.format_exc())
        return False

def find_book_by_id_or_title(keyword: str) -> Optional[Dict]:
    try:
        db = get_connection()
        query = {"$or": []}
        if keyword.isdigit():
            query["$or"].append({"id": int(keyword)})
        if keyword:
            query["$or"].append({"title": {"$regex": keyword}})
            query["$or"].append({"author": {"$regex": keyword}})
            query["$or"].append({"publisher": {"$regex": keyword}})
        if not query["$or"]:
            return None
        book = db.books.find_one(query)
        return book
    except Exception as e:
        print(f"[ERROR] find_book_by_id_or_title: {e}")
        print(traceback.format_exc())
        return None

def get_user_by_username(username):
    try:
        db = get_connection()
        return db.users.find_one({"username": username})
    except Exception as e:
        print(f"数据库查询出错: {e}")
        return None

def get_borrowed_count(username):
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return 0
        return db.borrowrecords.count_documents({"user_id": str(user["_id"]), "return_date": None})
    except Exception as e:
        print(f"获取借阅数量出错: {e}")
        return 0

def create_user(username: str, password: str, phone: str, email: str, role: str = 'user', max_borrow: int = 2) -> bool:
    try:
        db = get_connection()
        db.users.insert_one({
            "username": username,
            "password": password,
            "role": role,
            "phone": phone,
            "email": email,
            "max_borrow": max_borrow
        })
        return True
    except Exception as e:
        print(f"[ERROR] create_user: {e}")
        return False