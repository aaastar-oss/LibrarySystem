from pymongo import MongoClient

MONGO_URI = "mongodb+srv://aaastar-oss:ayuninger5201314.@cluster0.cw44yd7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "library"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

try:
    result = db.books.delete_many({})
    print(f"已删除 {result.deleted_count} 本图书")
except Exception as e:
    print("删除数据时出错:", str(e))
finally:
    client.close()
