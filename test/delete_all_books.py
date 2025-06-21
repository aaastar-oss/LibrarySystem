from pymongo import MongoClient
from datetime import datetime, timedelta

MONGO_URI = "mongodb+srv://aaastar-oss:ayuninger5201314.@cluster0.cw44yd7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "library"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

try:
    result = db.books.delete_many({})
    print(f"已删除 {result.deleted_count} 本图书")
except Exception as e:
    print("删除数据时出错:", str(e))

# 添加一本超期未还的图书用于测试
try:
    overdue_book = {
        "title": "测试超期图书",
        "user_id": "44444",
        "borrow_date": datetime.now() - timedelta(days=30),
        "due_date": datetime.now() - timedelta(days=15),  # 15天前到期
        "status": "borrowed"
    }
    db.books.insert_one(overdue_book)
    print("已添加一本超期未还的测试图书。")
except Exception as e:
    print("添加测试图书时出错:", str(e))
finally:
    client.close()
