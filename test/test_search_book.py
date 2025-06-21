from services import user_service

def test_search():
    print("空字符串搜索：", user_service.search_book(""))
    print("特殊字符搜索：", user_service.search_book("@#$%"))
    print("不存在的书名：", user_service.search_book("不存在的书名123456"))

if __name__ == "__main__":
    test_search()
