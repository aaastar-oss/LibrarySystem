# services/admin_service.py
from db import database_admin  # 假设database.py在db目录下，且已正确导入

def add_book(book: dict) -> bool:
    print(f"[add_book] 尝试添加图书：{book}")
    try:
        result = database_admin.insert_book(book)
        print(f"[add_book] 添加结果：{result}")
        return result
    except Exception as e:
        print(f"[add_book] 异常错误：{e}")
        return False


def delete_book(book_id: str) -> bool:
    print(f"[delete_book] 尝试删除图书ID：{book_id}")
    try:
        if not database_admin.book_exists(book_id):
            print(f"[delete_book] 图书ID不存在：{book_id}")
            return False
        result = database_admin.delete_book_by_id(book_id)
        print(f"[delete_book] 删除结果：{result}")
        return result
    except Exception as e:
        print(f"[delete_book] 异常错误：{e}")
        return False


def modify_book(book_id: str, new_data: dict) -> bool:
    print(f"[modify_book] 尝试修改图书ID：{book_id}，新数据：{new_data}")
    try:
        if not database_admin.book_exists(book_id):
            print(f"[modify_book] 图书ID不存在：{book_id}")
            return False
        result = database_admin.update_book_fields(book_id, new_data)
        print(f"[modify_book] 修改结果：{result}")
        return result
    except Exception as e:
        print(f"[modify_book] 异常错误：{e}")
        return False


def query_book(keyword: str):
    print(f"[query_book] 查询关键字：{keyword}")
    try:
        result = database_admin.find_book_by_id_or_title(keyword)
        print(f"[query_book] 查询结果：{result}")
        if result:
            return [result]
        else:
            return []
    except Exception as e:
        print(f"[query_book] 异常错误：{e}")
        return []


def query_user(username: str):
    print(f"[query_user] 查询用户借阅记录，用户名：{username}")
    try:
        result = database_admin.find_user_borrow_records(username)
        print(f"[query_user] 查询结果：{result}")
        return result
    except Exception as e:
        print(f"[query_user] 异常错误：{e}")
        return None


def query_all_books():
    print(f"[query_all_books] 查询所有图书信息")
    try:
        result = database_admin.get_all_books_fullinfo()
        print(f"[query_all_books] 查询结果条数：{len(result) if result else 0}")
        return result
    except Exception as e:
        print(f"[query_all_books] 异常错误：{e}")
        return []
