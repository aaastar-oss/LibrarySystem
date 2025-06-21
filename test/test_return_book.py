from services import user_service

def test_return(username, book_id):
    # 先借书
    user_service.borrow_book(username, book_id)
    # 再归还
    result = user_service.return_book(username, book_id)
    print("归还图书是否成功（应为True）：", result)

if __name__ == "__main__":
    test_return("44444", 3)
