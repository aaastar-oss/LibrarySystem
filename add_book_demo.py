from services import admin_service

if __name__ == "__main__":
    # 填写你要添加的图书信息
    book = {
        "title": "示例书籍",
        "author": "张三",
        "publisher": "测试出版社",
        "publish_date": "2024-06-01",  # 改为 publish_date
        "price": 88.8
    }
    result = admin_service.add_book(book)
    print("添加结果：", result)
