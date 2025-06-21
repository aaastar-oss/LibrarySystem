from pymongo import MongoClient
from datetime import datetime, timedelta

MONGO_URI = "mongodb+srv://aaastar-oss:ayuninger5201314.@cluster0.cw44yd7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "library"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

try:
    # 清空所有借阅记录
    db.borrowrecords.delete_many({})
    print("已清空所有借阅记录。")

    # 查找一本可用的书
    book = db.books.find_one({"available_copies": {"$gt": 0}})
    if not book:
        print("没有可用图书，无法插入超期借阅记录。")
    else:
        # 获取用户44444的_id
        user = db.users.find_one({"username": "test_user"})
        if not user:
            print("用户44444不存在。")
        else:
            overdue_record = {
                "user_id": str(user["_id"]),
                "book_id": str(book["id"]),
                "borrow_date": datetime.now() - timedelta(days=30),
                "due_date": datetime.now() - timedelta(days=15),  # 15天前到期
                "return_date": None
            }
            db.borrowrecords.insert_one(overdue_record)
            print(f"已为用户44444插入一本超期未还的借阅记录，书籍编号：{book['id']}")
except Exception as e:
    print("操作出错:", str(e))
finally:
    client.close()
