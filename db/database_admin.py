# /db/database.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional, List, Dict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def get_connection():
    client = MongoClient(config.MONGO_URI)
    db = client[config.MONGO_DB]
    return db

def get_next_book_id(db):
    """获取下一个自增编号"""
    last = db.books.find_one(sort=[("id", -1)])
    return (last["id"] + 1) if last and "id" in last else 1

def insert_book(book: Dict) -> Optional[str]:
    try:
        db = get_connection()
        # 生成自增编号
        book_id = get_next_book_id(db)
        doc = {
            "id": book_id,  # 新增编号字段
            "title": book['title'],
            "author": book['author'],
            "publisher": book['publisher'],
            "publish_date": book['publish_date'],
            "price": book['price'],
            "total_copies": book.get('total_copies', 3),
            "available_copies": book.get('available_copies', 3),
            "category": book.get('category', ''),
            "isbn": book.get('isbn', '')
        }
        result = db.books.insert_one(doc)
        return str(book_id)
    except Exception as e:
        print(f"[ERROR] insert_book: {e}")
        return None

def book_exists(book_id: str) -> bool:
    try:
        db = get_connection()
        # 用id字段判断
        return db.books.count_documents({"id": int(book_id)}) > 0
    except Exception as e:
        print(f"[ERROR] book_exists: {e}")
        return False

def delete_book_by_id(book_id: str) -> bool:
    try:
        db = get_connection()
        result = db.books.delete_one({"id": int(book_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"[ERROR] delete_book_by_id: {e}")
        return False

def update_book_fields(book_id: str, new_data: Dict) -> bool:
    if not new_data:
        return False
    if 'title' in new_data:
        del new_data['title']
    try:
        db = get_connection()
        result = db.books.update_one({"id": int(book_id)}, {"$set": new_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"[ERROR] update_book_fields: {e}")
        return False

def find_book_by_id_or_title(keyword: str) -> Optional[Dict]:
    try:
        db = get_connection()
        query = {"$or": []}
        if keyword.isdigit():
            query["$or"].append({"id": int(keyword)})
        # 仅当keyword非空时添加模糊条件
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
        return None

def find_user_borrow_records(username: str) -> List[Dict]:
    try:
        db = get_connection()
        user = db.users.find_one({"username": username})
        if not user:
            return []
        records = db.borrowrecords.find({"user_id": str(user["_id"]), "return_date": None})
        result = []
        for rec in records:
            book = db.books.find_one({"id": int(rec["book_id"])})
            if book:
                result.append({
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "borrow_date": rec.get("borrow_date"),
                    "return_date": rec.get("return_date")
                })
        return result
    except Exception as e:
        print(f"[ERROR] find_user_borrow_records: {e}")
        return []

def get_all_books_fullinfo() -> List[Dict]:
    try:
        db = get_connection()
        books = db.books.find()
        result = []
        for book in books:
            result.append({
                "id": book.get("id"),
                "title": book.get("title"),
                "author": book.get("author"),
                "publisher": book.get("publisher"),
                "publish_date": book.get("publish_date"),
                "price": book.get("price"),
                "available_copies": book.get("available_copies", 0),  # 修正字段名
                "total_copies": book.get("total_copies", 0),
                "borrowed": book.get("total_copies", 0) - book.get("available_copies", 0),
                "isbn": book.get("isbn", ""),
                "category": book.get("category", "")
            })
        return result
    except Exception as e:
        print(f"[ERROR] get_all_books_fullinfo: {e}")
        return []
