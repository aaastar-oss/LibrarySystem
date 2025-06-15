# enhanced_user_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from services import user_service
import traceback

FONT_TITLE = ("微软雅黑", 20, "bold")
FONT_LABEL = ("微软雅黑", 12)
FONT_BUTTON = ("微软雅黑", 12)
COLOR_BG = "#ffffff"
COLOR_BTN_PRIMARY = "#3498db"
COLOR_BTN_PRIMARY_ACTIVE = "#2980b9"
COLOR_BTN_SUCCESS = "#27ae60"
COLOR_BTN_SUCCESS_ACTIVE = "#1e8449"
COLOR_BTN_DISABLED = "#bdc3c7"
COLOR_TEXT = "#2c3e50"
COLOR_FOOTER = "#999999"

class UserGUI(tk.Tk):
    def __init__(self, username=None):
        super().__init__()
        self.title("图书管理系统 - 用户")
        self.geometry("500x600")
        self.configure(bg=COLOR_BG)
        self.username = username  # 全局用户名

        self.frames = {}
        for F in (MenuPage, BorrowPage, ReturnPage, AvailablePage, MyBooksPage, SearchBookPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        footer = tk.Label(self, text="© 2025 图书管理系统", font=("微软雅黑", 10), bg=COLOR_BG, fg=COLOR_FOOTER)
        footer.place(relx=0.5, rely=1.0, anchor="s", y=-5)

        self.show_login()

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            if hasattr(frame, "update_data"):
                frame.update_data()

    def show_login(self):
        login = tk.Toplevel(self)
        login.title("登录")
        login.geometry("300x150")
        login.configure(bg=COLOR_BG)

        tk.Label(login, text="请输入用户名：", font=FONT_LABEL, bg=COLOR_BG).pack(pady=10)
        entry = tk.Entry(login, width=25, font=FONT_LABEL)
        entry.pack()

        def confirm():
            name = entry.get().strip()
            if name:
                self.username = name
                login.destroy()
                self.show_frame("MenuPage")
            else:
                messagebox.showwarning("输入错误", "用户名不能为空")

        tk.Button(login, text="确定", command=confirm,
                  font=FONT_BUTTON, bg=COLOR_BTN_PRIMARY, fg="white",
                  activebackground=COLOR_BTN_PRIMARY_ACTIVE, relief="flat").pack(pady=10)

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="用户菜单", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(40, 30))
        btn_config = {"width": 25, "height": 2, "font": FONT_BUTTON,
                      "bg": COLOR_BTN_PRIMARY, "fg": "white", "activebackground": COLOR_BTN_PRIMARY_ACTIVE,
                      "activeforeground": "white", "relief": "flat", "bd": 0}

        buttons = [
            ("借阅图书", lambda: controller.show_frame("BorrowPage")),
            ("归还图书", lambda: controller.show_frame("ReturnPage")),
            ("查询可借图书", lambda: controller.show_frame("AvailablePage")),
            ("查询我的借阅信息", lambda: controller.show_frame("MyBooksPage")),
            ("查询图书详情", lambda: controller.show_frame("SearchBookPage")),
            ("退出", controller.quit)
        ]
        for label, cmd in buttons:
            tk.Button(self, text=label, command=cmd, **btn_config).pack(pady=5)

class UserBookInputFrame(tk.Frame):
    def __init__(self, parent, controller, action_text, action_command):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.action_command = action_command

        tk.Label(self, text=action_text, font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=15)
        tk.Label(self, text="图书编号：", font=FONT_LABEL, bg=COLOR_BG).pack(pady=5)
        self.book_id_entry = tk.Entry(self, width=25, font=FONT_LABEL)
        self.book_id_entry.pack()

        tk.Button(self, text=action_text, command=self.action_command,
                  font=FONT_BUTTON, bg=COLOR_BTN_PRIMARY, fg="white",
                  activebackground=COLOR_BTN_PRIMARY_ACTIVE, relief="flat", bd=0, width=15).pack(pady=15)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

class BorrowPage(UserBookInputFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "确认借阅", self.do_borrow)

    def do_borrow(self):
        book_id = self.book_id_entry.get().strip()
        username = self.controller.username

        if not book_id.isdigit():
            messagebox.showwarning("输入错误", "图书编号必须是数字")
            return

        try:
            result = user_service.borrow_book(username, book_id)
            if result is True:
                messagebox.showinfo("成功", "借书成功")
                self.book_id_entry.delete(0, tk.END)
            elif result == "overdue":
                messagebox.showerror("失败", "有超期图书未归还，无法借书")
            else:
                messagebox.showerror("失败", "借书失败，可能已借出或超限")
        except Exception as e:
            messagebox.showerror("错误", f"出错：{e}")

class ReturnPage(UserBookInputFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "确认归还", self.do_return)

    def do_return(self):
        book_id = self.book_id_entry.get().strip()
        username = self.controller.username

        if not book_id.isdigit():
            messagebox.showwarning("输入错误", "图书编号必须是数字")
            return

        try:
            success = user_service.return_book(username, book_id)
            if success:
                messagebox.showinfo("成功", "还书成功")
                self.book_id_entry.delete(0, tk.END)
            else:
                messagebox.showerror("失败", "还书失败，可能未借该书")
        except Exception as e:
            messagebox.showerror("错误", f"出错：{e}")

class AvailablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        tk.Label(self, text="可借图书", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("编号", "书名", "作者", "剩余"), show="headings")
        for col in ("编号", "书名", "作者", "剩余"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Button(self, text="刷新列表", command=self.update_data,
                  font=FONT_BUTTON, bg=COLOR_BTN_SUCCESS, fg="white",
                  activebackground=COLOR_BTN_SUCCESS_ACTIVE, relief="flat", bd=0).pack(pady=5)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

    def update_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            books = user_service.query_books()
            if books:  # 确保有数据
                for book in books:
                # 使用字典键访问数据
                    self.tree.insert('', tk.END, values=(
                    book.get('id', ''),
                    book.get('title', ''),
                    book.get('author', ''),
                    book.get('available_copies', 0)  # 确保字段名匹配
                    ))
            else:
                messagebox.showinfo("提示", "没有可借图书")
        except Exception as e:
            messagebox.showerror("错误", f"查询图书时出错：{e}")
        print(f"详细错误：{e}")  # 打印详细错误信息

class MyBooksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="我的借阅信息", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=15)
        self.text = tk.Text(self, font=FONT_LABEL, height=20, wrap="word")
        self.text.pack(fill='both', expand=True, padx=15, pady=10)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

    def update_data(self):
        username = self.controller.username
        self.text.delete("1.0", tk.END)
        try:
            books = user_service.get_user_borrowed(username)
            if books:
                for book in books:
                    # 使用字典键访问数据
                    self.text.insert(tk.END, 
                        f"编号: {book.get('id', 'N/A')}, "
                        f"书名: {book.get('title', '未知')}, "
                        f"到期: {book.get('due_date', '未知')}\n"
                    )
            else:
                self.text.insert(tk.END, "暂无借阅记录\n")
        except Exception as e:
            messagebox.showerror("错误", f"查询借阅信息时出错：{e}")
            print(f"详细错误：{e}\n{traceback.format_exc()}")  # 打印详细错误

class SearchBookPage(tk.Frame):      
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="查询图书信息", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=10)
        self.entry = tk.Entry(self, font=FONT_LABEL, width=30)
        self.entry.pack(pady=5)

        tk.Button(self, text="查询", command=self.search_book,
                  font=FONT_BUTTON, bg=COLOR_BTN_PRIMARY, fg="white",
                  activebackground=COLOR_BTN_PRIMARY_ACTIVE, relief="flat", bd=0, width=15).pack(pady=10)

        self.text = tk.Text(self, font=FONT_LABEL, height=20, wrap="word")
        self.text.pack(fill='both', expand=True, padx=15, pady=5)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

    def search_book(self):
        keyword = self.entry.get().strip()
        self.text.delete("1.0", tk.END)
        if not keyword:
            messagebox.showwarning("输入错误", "请输入图书编号或书名")
            return
        try:
            # 修改这里：将 user_service.query_book 改为 user_service.search_book
            result = user_service.search_book(keyword)
            if result:
                # 根据实际返回的字段名调整以下代码
                info = (f"编号: {result.get('id', 'N/A')}\n"
                        f"书名: {result.get('title', '未知')}\n"
                        f"作者: {result.get('author', '未知')}\n"
                        f"出版社: {result.get('publisher', '未知')}\n"
                        f"出版日期: {result.get('publish_date', '未知')}\n"
                        f"价格: ￥{result.get('price', 0):.2f}\n"
                        f"总副本: {result.get('total_copies', 0)}\n"
                        f"剩余副本: {result.get('available_copies', 0)}\n")
                self.text.insert(tk.END, info)
            else:
                self.text.insert(tk.END, "未找到该图书\n")
        except Exception as e:
            messagebox.showerror("错误", f"查询图书信息出错：{e}")

if __name__ == "__main__":
    app = UserGUI()
    app.mainloop()
