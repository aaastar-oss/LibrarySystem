import tkinter as tk
from tkinter import messagebox
from services import user_service

# 统一字体和颜色配置，方便全局调整
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
    def __init__(self, start_page="MenuPage"):
        super().__init__()
        self.title("图书管理系统 - 用户")
        self.geometry("400x550")
        self.configure(bg=COLOR_BG)

        self.frames = {}
        for F in (MenuPage, BorrowPage, ReturnPage, AvailablePage, MyBooksPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        footer = tk.Label(self, text="© 2025 图书管理系统", font=("微软雅黑", 10), bg=COLOR_BG, fg=COLOR_FOOTER)
        footer.place(relx=0.5, rely=1.0, anchor="s", y=-5)

        self.show_frame(start_page)

    def show_frame(self, page_name):
        print(f"[DEBUG] 显示页面: {page_name}")
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
        else:
            print(f"[ERROR] 未找到页面: {page_name}")

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="用户菜单", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(40, 30))

        btn_config = {
            "width": 25, "height": 2, "font": FONT_BUTTON,
            "bg": COLOR_BTN_PRIMARY, "fg": "white", "activebackground": COLOR_BTN_PRIMARY_ACTIVE,
            "activeforeground": "white", "relief": "flat", "bd": 0
        }

        buttons = [
            ("借阅图书", lambda: controller.show_frame("BorrowPage")),
            ("归还图书", lambda: controller.show_frame("ReturnPage")),
            ("查询可借图书", lambda: controller.show_frame("AvailablePage")),
            ("查询我的借阅信息", lambda: controller.show_frame("MyBooksPage")),
            ("退出", controller.quit)
        ]

        for label, cmd in buttons:
            tk.Button(self, text=label, command=cmd, **btn_config).pack(pady=10)

class UserBookInputFrame(tk.Frame):
    """
    通用借书/还书输入框框架
    """
    def __init__(self, parent, controller, action_text, action_command):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text=action_text, font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=15)

        tk.Label(self, text="用户名：", font=FONT_LABEL, bg=COLOR_BG).pack(pady=5)
        self.username_entry = tk.Entry(self, width=25, font=FONT_LABEL)
        self.username_entry.pack()

        tk.Label(self, text="图书编号：", font=FONT_LABEL, bg=COLOR_BG).pack(pady=5)
        self.book_id_entry = tk.Entry(self, width=25, font=FONT_LABEL)
        self.book_id_entry.pack()

        tk.Button(self, text=action_text, command=action_command,
                  font=FONT_BUTTON, bg=COLOR_BTN_PRIMARY, fg="white",
                  activebackground=COLOR_BTN_PRIMARY_ACTIVE, relief="flat", bd=0, width=15).pack(pady=15)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

class BorrowPage(UserBookInputFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "确认借阅", self.do_borrow)

    def do_borrow(self):
        username = self.username_entry.get().strip()
        book_id = self.book_id_entry.get().strip()

        if not username:
            messagebox.showwarning("输入错误", "用户名不能为空")
            return
        if not book_id:
            messagebox.showwarning("输入错误", "图书编号不能为空")
            return
        if not book_id.isdigit():
            messagebox.showwarning("输入错误", "图书编号必须是数字")
            return

        try:
            success = user_service.borrow_book(username, book_id)
            if success:
                messagebox.showinfo("成功", "借书成功")
                # 清空输入
                self.username_entry.delete(0, tk.END)
                self.book_id_entry.delete(0, tk.END)
            else:
                messagebox.showerror("失败", "借书失败，可能已借出或超限")
        except Exception as e:
            messagebox.showerror("错误", f"出错：{e}")

class ReturnPage(UserBookInputFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "确认归还", self.do_return)

    def do_return(self):
        username = self.username_entry.get().strip()
        book_id = self.book_id_entry.get().strip()

        if not username:
            messagebox.showwarning("输入错误", "用户名不能为空")
            return
        if not book_id:
            messagebox.showwarning("输入错误", "图书编号不能为空")
            return
        if not book_id.isdigit():
            messagebox.showwarning("输入错误", "图书编号必须是数字")
            return

        try:
            success = user_service.return_book(username, book_id)
            if success:
                messagebox.showinfo("成功", "还书成功")
                # 清空输入
                self.username_entry.delete(0, tk.END)
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

        frame_text = tk.Frame(self)
        frame_text.pack(fill='both', expand=True, padx=10, pady=10)

        self.text = tk.Text(frame_text, wrap='none', font=("微软雅黑", 11))
        self.text.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(frame_text, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

        tk.Button(self, text="刷新列表", command=self.load_books,
                  font=FONT_BUTTON, bg=COLOR_BTN_SUCCESS, fg="white",
                  activebackground=COLOR_BTN_SUCCESS_ACTIVE, relief="flat", bd=0, width=15).pack(pady=5)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

        self.load_books()

    def load_books(self):
        self.text.delete("1.0", tk.END)
        try:
            books = user_service.query_books()
            if books:
                for b in books:
                    self.text.insert(tk.END, f"编号:{b[0]}  书名:{b[1]}  作者:{b[2]}  剩余副本:{b[3]}\n")
            else:
                self.text.insert(tk.END, "暂无可借图书\n")
        except Exception as e:
            messagebox.showerror("错误", f"查询图书时出错：{e}")

class MyBooksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="我的借阅信息", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=15)

        tk.Label(self, text="用户名：", font=FONT_LABEL, bg=COLOR_BG).pack(pady=5)
        self.entry = tk.Entry(self, width=30, font=FONT_LABEL)
        self.entry.pack(pady=5)

        tk.Button(self, text="查询我的借阅", command=self.query_my_books,
                  font=FONT_BUTTON, bg=COLOR_BTN_PRIMARY, fg="white",
                  activebackground=COLOR_BTN_PRIMARY_ACTIVE, relief="flat", bd=0, width=18).pack(pady=10)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg=COLOR_BTN_DISABLED, fg="black", relief="flat").pack(pady=5)

    def query_my_books(self):
        username = self.entry.get().strip()
        if not username:
            messagebox.showwarning("输入错误", "请输入用户名")
            return

        try:
            books = user_service.get_user_borrowed(username)
            if books:
                info = "\n".join([f"编号: {b[0]}, 书名: {b[1]}, 到期: {b[2]}" for b in books])
                messagebox.showinfo("借阅信息", info)
            else:
                messagebox.showinfo("借阅信息", "暂无借阅记录")
        except Exception as e:
            messagebox.showerror("错误", f"查询借阅信息时出错：{e}")

if __name__ == "__main__":
    app = UserGUI()
    app.mainloop()
