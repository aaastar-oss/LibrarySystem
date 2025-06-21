import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import user_service

def test_borrow_limit(username, book_ids):
    # 先确保用户已借满2本
    for book_id in book_ids[:2]:
        user_service.borrow_book(username, book_id)
    # 尝试借第3本
    result = user_service.borrow_book(username, book_ids[2])
    print("借第3本书是否成功（应为False）：", result)

if __name__ == "__main__":
    # 用户测试用44444
    test_borrow_limit("22222", [1,2,3])
