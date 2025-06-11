import tkinter as tk
from tkinter import messagebox
from services import user_service


class UserGUI(tk.Tk):
    def __init__(self, start_page="MenuPage"):
        super().__init__()
        self.title("图书管理系统 - 用户")
        self.geometry("400x550")
        self.configure(bg="#ffffff")

        self.frames = {}
        for F in (MenuPage, BorrowPage, ReturnPage, AvailablePage, MyBooksPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        label = tk.Label(self, text="© 2025 图书管理系统", font=("微软雅黑", 10), bg="#ffffff", fg="#999999")
        label.place(relx=0.5, rely=1.0, anchor="s", y=-5)

        self.show_frame(start_page)

    def show_frame(self, page_name):
        print(f"[DEBUG] 显示页面: {page_name}")
        self.frames[page_name].tkraise()

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="用户菜单", font=("微软雅黑", 24, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(40, 30))

        btn_config = {
            "width": 25, "height": 2, "font": ("微软雅黑", 14),
            "bg": "#3498db", "fg": "white", "activebackground": "#2980b9",
            "activeforeground": "white", "relief": "flat", "bd": 0
        }

        buttons = [
            ("借阅图书", lambda: controller.show_frame("BorrowPage")),
            ("归还图书", lambda: controller.show_frame("ReturnPage")),
            ("查询可借图书", lambda: controller.show_frame("AvailablePage")),
            ("查询我的借阅信息", lambda: controller.show_frame("MyBooksPage")),
            ("退出", controller.quit)
        ]

        for label, command in buttons:
            tk.Button(self, text=label, command=command, **btn_config).pack(pady=10)


class BorrowPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="借阅图书", font=("微软雅黑", 20), bg="#ffffff").pack(pady=15)

        self.username_entry = tk.Entry(self, width=25, font=("微软雅黑", 12))
        self.book_id_entry = tk.Entry(self, width=25, font=("微软雅黑", 12))

        tk.Label(self, text="用户名：", font=("微软雅黑", 12), bg="#ffffff").pack(pady=5)
        self.username_entry.pack()

        tk.Label(self, text="图书编号：", font=("微软雅黑", 12), bg="#ffffff").pack(pady=5)
        self.book_id_entry.pack()

        tk.Button(self, text="确认借阅", command=self.do_borrow,
                  font=("微软雅黑", 12), bg="#3498db", fg="white",
                  activebackground="#2980b9", relief="flat", bd=0, width=15).pack(pady=15)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg="#bdc3c7", fg="black", relief="flat").pack(pady=5)

    def do_borrow(self):
        username = self.username_entry.get().strip()
        book_id = self.book_id_entry.get().strip()
        if username and book_id:
            try:
                if user_service.borrow_book(username, book_id):
                    messagebox.showinfo("成功", "借书成功")
                else:
                    messagebox.showerror("失败", "借书失败，可能已借出或超限")
            except Exception as e:
                messagebox.showerror("错误", f"出错：{e}")
        else:
            messagebox.showwarning("输入错误", "请填写完整信息")


class ReturnPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="归还图书", font=("微软雅黑", 20), bg="#ffffff").pack(pady=15)

        self.username_entry = tk.Entry(self, width=25, font=("微软雅黑", 12))
        self.book_id_entry = tk.Entry(self, width=25, font=("微软雅黑", 12))

        tk.Label(self, text="用户名：", font=("微软雅黑", 12), bg="#ffffff").pack(pady=5)
        self.username_entry.pack()

        tk.Label(self, text="图书编号：", font=("微软雅黑", 12), bg="#ffffff").pack(pady=5)
        self.book_id_entry.pack()

        tk.Button(self, text="确认归还", command=self.do_return,
                  font=("微软雅黑", 12), bg="#3498db", fg="white",
                  activebackground="#2980b9", relief="flat", bd=0, width=15).pack(pady=15)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg="#bdc3c7", fg="black", relief="flat").pack(pady=5)

    def do_return(self):
        username = self.username_entry.get().strip()
        book_id = self.book_id_entry.get().strip()
        if username and book_id:
            try:
                if user_service.return_book(username, book_id):
                    messagebox.showinfo("成功", "还书成功")
                else:
                    messagebox.showerror("失败", "还书失败，可能未借该书")
            except Exception as e:
                messagebox.showerror("错误", f"出错：{e}")
        else:
            messagebox.showwarning("输入错误", "请填写完整信息")


class AvailablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="可借图书", font=("微软雅黑", 20), bg="#ffffff").pack(pady=10)

        self.text = tk.Text(self, wrap='none', font=("微软雅黑", 11))
        self.text.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Button(self, text="刷新列表", command=self.load_books,
                  font=("微软雅黑", 12), bg="#27ae60", fg="white",
                  activebackground="#1e8449", relief="flat", bd=0, width=15).pack(pady=5)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg="#bdc3c7", fg="black", relief="flat").pack(pady=5)

        self.load_books()

    def load_books(self):
        self.text.delete("1.0", tk.END)
        books = user_service.query_books()
        if books:
            for b in books:
                self.text.insert(tk.END, f"编号:{b[0]}  书名:{b[1]}  作者:{b[2]}  剩余副本:{b[3]}\n")
        else:
            self.text.insert(tk.END, "暂无可借图书")


class MyBooksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="我的借阅信息", font=("微软雅黑", 20), bg="#ffffff").pack(pady=15)

        self.entry = tk.Entry(self, width=30, font=("微软雅黑", 12))
        self.entry.pack(pady=5)

        tk.Button(self, text="查询我的借阅", command=self.query_my_books,
                  font=("微软雅黑", 12), bg="#3498db", fg="white",
                  activebackground="#2980b9", relief="flat", bd=0, width=18).pack(pady=10)

        tk.Button(self, text="返回菜单", command=lambda: controller.show_frame("MenuPage"),
                  font=("微软雅黑", 10), bg="#bdc3c7", fg="black", relief="flat").pack(pady=5)

    def query_my_books(self):
        username = self.entry.get().strip()
        if username:
            books = user_service.get_user_borrowed(username)
            if books:
                info = "\n".join([f"编号: {b[0]}, 书名: {b[1]}, 到期: {b[2]}" for b in books])
                messagebox.showinfo("借阅信息", info)
            else:
                messagebox.showinfo("借阅信息", "暂无借阅记录")
        else:
            messagebox.showwarning("输入错误", "请输入用户名")


if __name__ == "__main__":
    app = UserGUI()
    app.mainloop()