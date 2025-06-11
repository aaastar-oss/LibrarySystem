import tkinter as tk
from services import admin_service  # 导入业务逻辑模块


# 全局UI配置
BG_COLOR = "#ffffff"
FONT_TITLE = ("微软雅黑", 24, "bold")
FONT_LABEL = ("微软雅黑", 14)
FONT_BUTTON = ("微软雅黑", 14)
BTN_BG = "#3498db"
BTN_FG = "white"
BTN_ACTIVE_BG = "#2980b9"
BTN_ACTIVE_FG = "white"
STATUS_FG_ERROR = "#e74c3c"
STATUS_FG_SUCCESS = "#27ae60"


class AdminGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图书管理系统 - 管理员")
        self.geometry("600x720")
        self.configure(bg=BG_COLOR)

        self.frames = {}

        # 初始化所有页面Frame
        for F in (MenuPage, AddBookPage, DeleteBookPage, ModifyBookPage, QueryBookPage, QueryUserPage, OverviewBooksPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        # 状态栏放主窗口底部，所有页面共用
        self.status_label = tk.Label(self, text="", font=FONT_LABEL, bg=BG_COLOR, fg=STATUS_FG_ERROR)
        self.status_label.pack(side="bottom", pady=10)

        # 底部版权
        tk.Label(self, text="© 2025 图书管理系统", font=("微软雅黑", 10), bg=BG_COLOR, fg="#999999").pack(side="bottom", pady=5)

        self.show_frame("MenuPage")

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, "update_data"):
            frame.update_data(**kwargs)
        frame.tkraise()

    def set_status(self, msg, color=STATUS_FG_ERROR):
        self.status_label.config(text=msg, fg=color)


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        title_label = tk.Label(self, text="管理员菜单", font=FONT_TITLE, fg="#2c3e50", bg=BG_COLOR)
        title_label.pack(pady=(50, 40))

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        btn_config = {
            "width": 28,
            "height": 2,
            "font": FONT_BUTTON,
            "bg": BTN_BG,
            "fg": BTN_FG,
            "activebackground": BTN_ACTIVE_BG,
            "activeforeground": BTN_ACTIVE_FG,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2"
        }

        buttons = [
            ("录入图书", lambda: controller.show_frame("AddBookPage")),
            ("删除图书", lambda: controller.show_frame("DeleteBookPage")),
            ("修改图书信息", lambda: controller.show_frame("ModifyBookPage")),
            ("查询图书信息和状态", lambda: controller.show_frame("QueryBookPage")),
            ("查询用户借书状态", lambda: controller.show_frame("QueryUserPage")),
            ("总览图书信息和状态", lambda: controller.show_frame("OverviewBooksPage")),
            ("退出系统", controller.quit)
        ]

        for label, command in buttons:
            btn = tk.Button(btn_frame, text=label, command=command, **btn_config)
            btn.pack(pady=10)


class AddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="录入图书", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)

        labels = ["编号", "书名", "作者", "出版社", "出版日期", "价格"]
        self.entries = []

        form_frame = tk.Frame(self, bg=BG_COLOR)
        form_frame.pack(pady=10)

        for i, label_text in enumerate(labels):
            tk.Label(form_frame, text=label_text, font=FONT_LABEL, bg=BG_COLOR).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            entry = tk.Entry(form_frame, width=30, font=FONT_LABEL)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries.append(entry)

        self.status = tk.Label(self, text="", fg=STATUS_FG_ERROR, bg=BG_COLOR, font=FONT_LABEL)
        self.status.pack(pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="保存", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.save_book).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def save_book(self):
        data = [e.get().strip() for e in self.entries]
        if all(data):
            try:
                book = {
                    "id": data[0],
                    "title": data[1],
                    "author": data[2],
                    "publisher": data[3],
                    "pub_date": data[4],
                    "price": float(data[5])
                }
                admin_service.add_book(book)
                self.status.config(text="图书已成功录入！", fg=STATUS_FG_SUCCESS)
                self.controller.set_status("录入图书成功", color=STATUS_FG_SUCCESS)
                self.after(1500, self.clear_and_return)
            except Exception as e:
                self.status.config(text=f"录入失败：{e}", fg=STATUS_FG_ERROR)
                self.controller.set_status(f"录入失败：{e}")
        else:
            self.status.config(text="请填写所有字段！", fg=STATUS_FG_ERROR)
            self.controller.set_status("录入图书失败：输入不完整")

    def clear_and_return(self):
        for e in self.entries:
            e.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")


class DeleteBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="删除图书", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)
        tk.Label(self, text="图书编号：", font=FONT_LABEL, bg=BG_COLOR).pack(pady=10)

        self.entry = tk.Entry(self, width=30, font=FONT_LABEL)
        self.entry.pack()

        self.status = tk.Label(self, text="", fg=STATUS_FG_ERROR, bg=BG_COLOR, font=FONT_LABEL)
        self.status.pack(pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="删除", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.do_delete).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def do_delete(self):
        book_id = self.entry.get().strip()
        if book_id:
            success = admin_service.delete_book(book_id)
            if success:
                self.status.config(text=f"图书 {book_id} 删除成功", fg=STATUS_FG_SUCCESS)
                self.controller.set_status(f"删除图书 {book_id} 成功", color=STATUS_FG_SUCCESS)
                self.after(1500, self.clear_and_return)
            else:
                self.status.config(text=f"图书 {book_id} 不存在", fg=STATUS_FG_ERROR)
                self.controller.set_status(f"删除失败：图书 {book_id} 不存在")
        else:
            self.status.config(text="请输入图书编号", fg=STATUS_FG_ERROR)
            self.controller.set_status("删除失败：请输入图书编号")

    def clear_and_return(self):
        self.entry.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")


class ModifyBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="修改图书信息", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)

        form_frame = tk.Frame(self, bg=BG_COLOR)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="请输入图书编号：", font=FONT_LABEL, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=8, sticky='e')
        self.entry_id = tk.Entry(form_frame, width=30, font=FONT_LABEL)
        self.entry_id.grid(row=0, column=1, padx=10, pady=8)

        labels = ["作者", "出版社", "出版日期", "价格"]
        self.entries = []

        for i, label_text in enumerate(labels, start=1):
            tk.Label(form_frame, text=label_text, font=FONT_LABEL, bg=BG_COLOR).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            entry = tk.Entry(form_frame, width=30, font=FONT_LABEL)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries.append(entry)

        self.status = tk.Label(self, text="", fg=STATUS_FG_ERROR, bg=BG_COLOR, font=FONT_LABEL)
        self.status.pack(pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="修改", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.do_modify).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def do_modify(self):
        book_id = self.entry_id.get().strip()
        data = [e.get().strip() for e in self.entries]
        if book_id and all(data):
            try:
                new_data = {
                    "author": data[0],
                    "publisher": data[1],
                    "pub_date": data[2],
                    "price": float(data[3])
                }
                success = admin_service.modify_book(book_id, new_data)
                if success:
                    self.status.config(text=f"图书 {book_id} 信息已更新", fg=STATUS_FG_SUCCESS)
                    self.controller.set_status(f"修改图书 {book_id} 成功", color=STATUS_FG_SUCCESS)
                    self.after(1500, self.clear_and_return)
                else:
                    self.status.config(text=f"图书 {book_id} 不存在", fg=STATUS_FG_ERROR)
                    self.controller.set_status(f"修改失败：图书 {book_id} 不存在")
            except Exception as e:
                self.status.config(text=f"修改失败：{e}", fg=STATUS_FG_ERROR)
                self.controller.set_status(f"修改失败：{e}")
        else:
            self.status.config(text="请填写所有字段", fg=STATUS_FG_ERROR)
            self.controller.set_status("修改失败：输入不完整")

    def clear_and_return(self):
        self.entry_id.delete(0, tk.END)
        for e in self.entries:
            e.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")


class QueryBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="查询图书信息", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)
        tk.Label(self, text="请输入图书编号或书名：", font=FONT_LABEL, bg=BG_COLOR).pack(pady=10)

        self.entry = tk.Entry(self, width=35, font=FONT_LABEL)
        self.entry.pack()

        self.result_text = tk.Text(self, height=8, width=50, font=FONT_LABEL)
        self.result_text.pack(pady=10)

        self.status = tk.Label(self, text="", fg=STATUS_FG_ERROR, bg=BG_COLOR, font=FONT_LABEL)
        self.status.pack(pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="查询", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.do_query).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def do_query(self):
        keyword = self.entry.get().strip()
        self.result_text.delete('1.0', tk.END)
        if keyword:
            result = admin_service.query_book(keyword)
            if result:
                book_str = (f"编号: {result[0]}\n书名: {result[1]}\n作者: {result[2]}"
                            f"\n出版社: {result[3]}\n出版日期: {result[4]}\n价格: {result[5]}")
                self.result_text.insert(tk.END, book_str)
                self.status.config(text="")
                self.controller.set_status(f"查询图书 {keyword} 成功", color=STATUS_FG_SUCCESS)
            else:
                self.status.config(text="未找到该图书", fg=STATUS_FG_ERROR)
                self.controller.set_status("查询失败：未找到该图书")
        else:
            self.status.config(text="请输入图书编号或书名", fg=STATUS_FG_ERROR)
            self.controller.set_status("查询失败：请输入图书编号或书名")

    def update_data(self):
        # 每次进入页面清空输入和结果
        self.entry.delete(0, tk.END)
        self.result_text.delete('1.0', tk.END)
        self.status.config(text="")


class QueryUserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="查询用户借阅状态", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)
        tk.Label(self, text="请输入用户名：", font=FONT_LABEL, bg=BG_COLOR).pack(pady=10)

        self.entry = tk.Entry(self, width=35, font=FONT_LABEL)
        self.entry.pack()

        self.result_text = tk.Text(self, height=10, width=55, font=FONT_LABEL)
        self.result_text.pack(pady=10)

        self.status = tk.Label(self, text="", fg=STATUS_FG_ERROR, bg=BG_COLOR, font=FONT_LABEL)
        self.status.pack(pady=5)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="查询", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.do_query).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def do_query(self):
        username = self.entry.get().strip()
        self.result_text.delete('1.0', tk.END)
        if username:
            books = admin_service.query_user(username)
            if books:
                info = "\n".join([f"编号: {b[0]}, 书名: {b[1]}, 借阅日期: {b[2]}" for b in books])
                self.result_text.insert(tk.END, info)
                self.status.config(text="")
                self.controller.set_status(f"查询用户 {username} 借阅状态成功", color=STATUS_FG_SUCCESS)
            else:
                self.status.config(text="该用户无借阅记录或不存在", fg=STATUS_FG_ERROR)
                self.controller.set_status("查询失败：用户无借阅记录或不存在")
        else:
            self.status.config(text="请输入用户名", fg=STATUS_FG_ERROR)
            self.controller.set_status("查询失败：请输入用户名")

    def update_data(self):
        self.entry.delete(0, tk.END)
        self.result_text.delete('1.0', tk.END)
        self.status.config(text="")


class OverviewBooksPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="总览图书信息和状态", font=FONT_TITLE, bg=BG_COLOR).pack(pady=20)

        self.text = tk.Text(self, width=70, height=25, font=FONT_LABEL)
        self.text.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="刷新", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=self.refresh).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="返回菜单", width=12, font=FONT_BUTTON, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG,
                  relief="flat", bd=0, cursor="hand2", command=lambda: self.controller.show_frame("MenuPage")).grid(row=0, column=1, padx=10)

    def refresh(self):
        self.text.delete('1.0', tk.END)
        books = admin_service.get_all_books()
        if books:
            for b in books:
                line = (f"编号: {b[0]}, 书名: {b[1]}, 作者: {b[2]}, 出版社: {b[3]}, "
                        f"出版日期: {b[4]}, 价格: {b[5]}, 库存: {b[6]}, 已借出: {b[7]}\n")
                self.text.insert(tk.END, line)
            self.controller.set_status("图书信息刷新成功", color=STATUS_FG_SUCCESS)
        else:
            self.text.insert(tk.END, "暂无图书信息")
            self.controller.set_status("暂无图书信息", color=STATUS_FG_ERROR)

    def update_data(self):
        self.refresh()


if __name__ == "__main__":
    app = AdminGUI()
    app.mainloop()
