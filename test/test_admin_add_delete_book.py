from services import admin_service

def test_add_delete():
    admin_username = "33333"
    # 添加一本新书
    book = {
        "title": "边界测试书",
        "author": "测试作者",
        "publisher": "测试出版社",
        "publish_date": "2024-01-01",
        "price": 10.0
    }
    # 如果admin_service.add_book支持传递管理员账号，则如下，否则去掉admin_username参数
    book_id = admin_service.add_book(book, admin_username)
    print("添加新书返回的id：", book_id)
    # 删除不存在的书
    result = admin_service.delete_book("999999", admin_username)
    print("删除不存在的书（应为False）：", result)
    # 删除刚添加的书
    if book_id:
        result2 = admin_service.delete_book(book_id, admin_username)
        print("删除刚添加的书（应为True）：", result2)

if __name__ == "__main__":
    test_add_delete()
