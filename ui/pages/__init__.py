from .AddBookPage import AddBookPage
from .DeleteBookPage import DeleteBookPage
from .ModifyBookPage import ModifyBookPage
from .QueryBookPage import QueryBookPage
from .QueryUserPage import QueryUserPage
from .OverviewBooksPage import OverviewBooksPage
from .menu_page import MenuPage
from .borrow_page import BorrowPage
from .return_page import ReturnPage
from .available_page import AvailablePage
from .mybooks_page import MyBooksPage
from .search_page import SearchBookPage

__all__ = [
    "AddBookPage",
    "DeleteBookPage",
    "ModifyBookPage",
    "QueryBookPage",
    "QueryUserPage",
    "OverviewBooksPage",
    'MenuPage',
    'BorrowPage',
    'ReturnPage',
    'AvailablePage',
    'MyBooksPage',
    'SearchBookPage'
]