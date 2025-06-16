from pymongo import MongoClient
from datetime import datetime

# MongoDB连接配置
MONGO_URI = "mongodb+srv://aaastar-oss:ayuninger5201314.@cluster0.cw44yd7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "library"

# 创建MongoDB客户端
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# 20本书籍数据列表
books = [
    {
        "title": "Python编程从入门到精通",
        "author": "张明",
        "publisher": "电子工业出版社",
        "publish_date": "2023-05-15",
        "price": 89.9,
        "total_copies": 3,
        "available_copies": 3,
        "category": "编程",
        "isbn": "9787121423123"
    },
    {
        "title": "数据结构与算法分析",
        "author": "王伟",
        "publisher": "清华大学出版社",
        "publish_date": "2022-08-20",
        "price": 75.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "计算机科学",
        "isbn": "9787302587129"
    },
    {
        "title": "人工智能基础",
        "author": "李强",
        "publisher": "人民邮电出版社",
        "publish_date": "2023-01-10",
        "price": 68.5,
        "total_copies": 3,
        "available_copies": 3,
        "category": "人工智能",
        "isbn": "9787115587124"
    },
    {
        "title": "数据库系统概念",
        "author": "赵刚",
        "publisher": "机械工业出版社",
        "publish_date": "2021-11-05",
        "price": 99.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "数据库",
        "isbn": "9787111678125"
    },
    {
        "title": "计算机网络",
        "author": "刘芳",
        "publisher": "高等教育出版社",
        "publish_date": "2022-03-18",
        "price": 65.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "网络",
        "isbn": "9787040567126"
    },
    {
        "title": "机器学习实战",
        "author": "陈晨",
        "publisher": "人民邮电出版社",
        "publish_date": "2023-07-22",
        "price": 79.9,
        "total_copies": 3,
        "available_copies": 3,
        "category": "机器学习",
        "isbn": "9787115578123"
    },
    {
        "title": "Web开发权威指南",
        "author": "周杰",
        "publisher": "电子工业出版社",
        "publish_date": "2022-09-30",
        "price": 88.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "Web开发",
        "isbn": "9787121434129"
    },
    {
        "title": "操作系统设计与实现",
        "author": "吴斌",
        "publisher": "清华大学出版社",
        "publish_date": "2021-12-15",
        "price": 72.5,
        "total_copies": 3,
        "available_copies": 3,
        "category": "操作系统",
        "isbn": "9787302578127"
    },
    {
        "title": "软件工程实践",
        "author": "郑伟",
        "publisher": "机械工业出版社",
        "publish_date": "2023-04-05",
        "price": 85.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "软件工程",
        "isbn": "9787111687127"
    },
    {
        "title": "计算机组成原理",
        "author": "林涛",
        "publisher": "高等教育出版社",
        "publish_date": "2022-06-28",
        "price": 67.8,
        "total_copies": 3,
        "available_copies": 3,
        "category": "计算机基础",
        "isbn": "9787040577125"
    },
    {
        "title": "深度学习入门",
        "author": "黄明",
        "publisher": "人民邮电出版社",
        "publish_date": "2023-03-12",
        "price": 92.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "深度学习",
        "isbn": "9787115597126"
    },
    {
        "title": "算法导论",
        "author": "Thomas Cormen",
        "publisher": "机械工业出版社",
        "publish_date": "2020-10-20",
        "price": 128.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "算法",
        "isbn": "9787111407010"
    },
    {
        "title": "Python数据科学手册",
        "author": "Jake VanderPlas",
        "publisher": "人民邮电出版社",
        "publish_date": "2021-07-15",
        "price": 89.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "数据科学",
        "isbn": "9787115475893"
    },
    {
        "title": "JavaScript高级程序设计",
        "author": "Nicholas Zakas",
        "publisher": "人民邮电出版社",
        "publish_date": "2022-05-18",
        "price": 99.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "前端开发",
        "isbn": "9787115275790"
    },
    {
        "title": "黑客与画家",
        "author": "Paul Graham",
        "publisher": "人民邮电出版社",
        "publish_date": "2021-09-22",
        "price": 59.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "计算机文化",
        "isbn": "9787115282828"
    },
    {
        "title": "代码整洁之道",
        "author": "Robert Martin",
        "publisher": "人民邮电出版社",
        "publish_date": "2020-12-10",
        "price": 69.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "编程实践",
        "isbn": "9787115216878"
    },
    {
        "title": "设计模式",
        "author": "Erich Gamma",
        "publisher": "机械工业出版社",
        "publish_date": "2021-11-30",
        "price": 79.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "软件设计",
        "isbn": "9787111075752"
    },
    {
        "title": "计算机程序的构造和解释",
        "author": "Harold Abelson",
        "publisher": "机械工业出版社",
        "publish_date": "2022-02-14",
        "price": 65.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "编程基础",
        "isbn": "9787111135104"
    },
    {
        "title": "重构：改善既有代码的设计",
        "author": "Martin Fowler",
        "publisher": "人民邮电出版社",
        "publish_date": "2021-08-25",
        "price": 89.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "编程实践",
        "isbn": "9787115353689"
    },
    {
        "title": "人月神话",
        "author": "Fred Brooks",
        "publisher": "清华大学出版社",
        "publish_date": "2022-07-19",
        "price": 59.0,
        "total_copies": 3,
        "available_copies": 3,
        "category": "软件工程",
        "isbn": "9787302455100"
    }
]

def get_next_book_id(db):
    last = db.books.find_one(sort=[("id", -1)])
    return (last["id"] + 1) if last and "id" in last else 1

try:
    print(f"待插入书籍数量: {len(books)}")
    # 为每本书生成自增id
    for book in books:
        book['id'] = get_next_book_id(db)
        db.books.insert_one(book)
    print(f"成功插入{len(books)}本书籍")
except Exception as e:
    print("插入数据时出错:", str(e))
finally:
    client.close()