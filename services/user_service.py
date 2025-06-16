import traceback
from db import database_user

def query_books():
    print("[query_books] 查询所有可借图书")
    try:
        result = database_user.get_available_books()
        print(f"[query_books] 查询结果：{len(result)} 本图书")
        return result
    except Exception as e:
        print(f"[query_books] 异常：{e}")
        print(traceback.format_exc())
        return []

def get_user_borrowed(username: str):
    print(f"[get_user_borrowed] 查询用户借阅：{username}")
    try:
        result = database_user.get_user_borrowed_books(username)
        print(f"[get_user_borrowed] 借阅记录：{len(result)} 条")
        # result 里已包含 status 字段，前端直接用
        return result
    except Exception as e:
        print(f"[get_user_borrowed] 异常：{e}")
        print(traceback.format_exc())
        return []

def has_overdue_books(username: str) -> bool:
    print(f"[has_overdue_books] 检查用户是否有超期图书：{username}")
    try:
        result = database_user.check_user_overdue(username)
        print(f"[has_overdue_books] 检查结果：{result}")
        return result
    except Exception as e:
        print(f"[has_overdue_books] 异常：{e}")
        print(traceback.format_exc())
        return False

def borrow_book(username: str, book_id: str) -> bool:
    print(f"[borrow_book] 用户 {username} 尝试借书 {book_id}")
    try:
        if database_user.check_user_overdue(username):
            print("[borrow_book] 有超期图书，拒绝借阅")
            return False
        if not database_user.book_exists(book_id):
            print("[borrow_book] 图书不存在")
            return False
        if not database_user.is_book_available(book_id):
            print("[borrow_book] 副本不足")
            return False
        if database_user.user_borrow_count(username) >= 5:
            print("[borrow_book] 已借书达上限")
            return False
        result = database_user.insert_borrow_record(username, book_id)
        print(f"[borrow_book] 借阅操作结果：{result}")
        return result
    except Exception as e:
        print(f"[borrow_book] 异常：{e}")
        print(traceback.format_exc())
        return False

def return_book(username: str, book_id: str) -> bool:
    print(f"[return_book] 用户 {username} 尝试归还图书 {book_id}")
    try:
        result = database_user.return_book_record(username, book_id)
        print(f"[return_book] 归还操作结果：{result}")
        return result
    except Exception as e:
        print(f"[return_book] 异常：{e}")
        print(traceback.format_exc())
        return False

def search_book(keyword: str):
    print(f"[search_book] 用户查询关键字：{keyword}")
    try:
        db = database_user.get_connection()
        query = {"$or": []}
        if keyword.isdigit():
            query["$or"].append({"id": int(keyword)})
        if keyword:
            query["$or"].append({"title": {"$regex": keyword}})
            query["$or"].append({"author": {"$regex": keyword}})
            query["$or"].append({"publisher": {"$regex": keyword}})
        if not query["$or"]:
            return []
        result = db.books.find(query)
        books = [book for book in result if book]
        print(f"[search_book] 查询结果：{books}")
        return books
    except Exception as e:
        print(f"[search_book] 异常：{e}")
        print(traceback.format_exc())
        return []
    
def get_user_info(username):
    """获取用户详细信息 - 修正版本"""
    print(f"[get_user_info] 正在查询用户: {username}")
    try:
        # 获取用户基本信息
        user_data = database_user.get_user_by_username(username)
        if not user_data:
            print("[get_user_info] 用户不存在")
            return None
            
        # 获取借阅数量
        borrowed_count = database_user.user_borrow_count(username)
        
        return {
            'username': user_data['username'],
            'role': user_data['role'],
            'phone': user_data.get('phone', '未设置'),
            'email': user_data.get('email', '未设置'),
            'max_borrow': user_data.get('max_borrow', 5),
            'current_borrowed': borrowed_count,
            'register_time': '未知'  # 表中无注册时间字段
        }
        
    except Exception as e:
        print(f"[get_user_info] 查询出错: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"获取用户信息失败: {str(e)}")