# services/user_service.py

# 模拟图书数据库：图书ID -> [书名, 作者, 剩余副本数量]
_books = {
    "1001": ["Python编程", "张三", 3],
    "1002": ["数据结构", "李四", 2],
    "1003": ["操作系统", "王五", 1],
}

# 模拟用户借阅记录：用户名 -> {图书ID: 到期日期字符串}
_user_borrowed = {
    # "zhangsan": {"1001": "2025-06-20"},
}

from datetime import datetime, timedelta

def query_books():
    """返回所有剩余副本>0的图书列表，格式 [(id, 书名, 作者, 剩余副本), ...]"""
    result = []
    for book_id, info in _books.items():
        if info[2] > 0:
            result.append((book_id, info[0], info[1], info[2]))
    return result

def borrow_book(username, book_id):
    """用户借书，成功返回True，否则False"""
    # 1. 检查图书是否存在且有剩余
    if book_id not in _books or _books[book_id][2] <= 0:
        return False

    # 2. 检查用户是否已借该书（假设不允许重复借阅同一本书）
    user_books = _user_borrowed.get(username, {})
    if book_id in user_books:
        return False

    # 3. 用户借书数量限制，例如最多5本
    if len(user_books) >= 5:
        return False

    # 4. 借书成功，减少图书剩余，添加借阅记录，默认到期时间为30天后
    _books[book_id][2] -= 1
    due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    user_books[book_id] = due_date
    _user_borrowed[username] = user_books
    return True

def return_book(username, book_id):
    """用户还书，成功返回True，否则False"""
    user_books = _user_borrowed.get(username, {})
    if book_id not in user_books:
        return False

    # 还书成功，增加图书剩余，删除借阅记录
    _books[book_id][2] += 1
    del user_books[book_id]
    if not user_books:
        _user_borrowed.pop(username)
    else:
        _user_borrowed[username] = user_books
    return True

def get_user_borrowed(username):
    """返回用户借阅的图书信息列表 [(id, 书名, 到期日期), ...]，没有则返回空列表"""
    user_books = _user_borrowed.get(username, {})
    result = []
    for book_id, due_date in user_books.items():
        book_name = _books.get(book_id, ["未知书名"])[0]
        result.append((book_id, book_name, due_date))
    return result
