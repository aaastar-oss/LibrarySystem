import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import user_service

def test_overdue_block(username, book_id):
    # 假设数据库已插入一条超期未还记录
    can_borrow = user_service.borrow_book(username, book_id)
    print("有超期图书时借书是否被禁止（应为False）：", can_borrow)

if __name__ == "__main__":
    test_overdue_block("44444", 2)
