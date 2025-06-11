import tkinter as tk
from tkinter import messagebox
from services import user_service


class UserGUI:
    def __init__(self, master):
        self.master = master
        master.title("图书管理系统 - 用户")
        master.geometry("400x550")
        master.configure(bg="#f0f0f0")

        title_label = tk.Label(master, text="用户菜单", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(40, 30))

        buttons = [
            ("借阅图书", self.borrow_book),
            ("归还图书", self.return_book),
            ("查询可借图书", self.query_available_books),
            ("查询我的借阅信息", self.query_my_books),
            ("退出", master.quit)
        ]

        for label, command in buttons:
            btn = tk.Button(master, text=label, command=command,
                            width=30, height=2,
                            font=("Helvetica", 14),
                            bg="#4a90e2", fg="white",
                            activebackground="#357ABD", activeforeground="white",
                            relief="raised", bd=3)
            btn.pack(pady=10, padx=50)

    def borrow_book(self):
        window = tk.Toplevel(self.master)
        window.title("借阅图书")
        window.geometry("300x200")

        tk.Label(window, text="用户名：").pack(pady=5)
        username_entry = tk.Entry(window, width=25)
        username_entry.pack()

        tk.Label(window, text="图书编号：").pack(pady=5)
        book_id_entry = tk.Entry(window, width=25)
        book_id_entry.pack()

        def do_borrow():
            username = username_entry.get().strip()
            book_id = book_id_entry.get().strip()
            if username and book_id:
                try:
                    success = user_service.borrow_book(username, book_id)
                    if success:
                        messagebox.showinfo("成功", "借书成功")
                        window.destroy()
                    else:
                        messagebox.showerror("失败", "借书失败，可能是图书已借出或借阅超限")
                except Exception as e:
                    messagebox.showerror("错误", f"借书出错：{e}")
            else:
                messagebox.showwarning("输入错误", "请填写完整信息")

        tk.Button(window, text="借阅", command=do_borrow).pack(pady=10)

    def return_book(self):
        window = tk.Toplevel(self.master)
        window.title("归还图书")
        window.geometry("300x200")

        tk.Label(window, text="用户名：").pack(pady=5)
        username_entry = tk.Entry(window, width=25)
        username_entry.pack()

        tk.Label(window, text="图书编号：").pack(pady=5)
        book_id_entry = tk.Entry(window, width=25)
        book_id_entry.pack()

        def do_return():
            username = username_entry.get().strip()
            book_id = book_id_entry.get().strip()
            if username and book_id:
                try:
                    success = user_service.return_book(username, book_id)
                    if success:
                        messagebox.showinfo("成功", "还书成功")
                        window.destroy()
                    else:
                        messagebox.showerror("失败", "还书失败，可能未借该书")
                except Exception as e:
                    messagebox.showerror("错误", f"还书出错：{e}")
            else:
                messagebox.showwarning("输入错误", "请填写完整信息")

        tk.Button(window, text="归还", command=do_return).pack(pady=10)

    def query_available_books(self):
        books = user_service.query_books()
        window = tk.Toplevel(self.master)
        window.title("可借图书")
        window.geometry("600x400")

        text = tk.Text(window, wrap='none')
        text.pack(fill='both', expand=True)

        if books:
            for b in books:
                text.insert(tk.END, f"编号:{b[0]} 书名:{b[1]} 作者:{b[2]} 剩余副本:{b[3]}\n")
        else:
            text.insert(tk.END, "暂无可借图书")

    def query_my_books(self):
        window = tk.Toplevel(self.master)
        window.title("我的借阅信息")
        window.geometry("350x200")

        tk.Label(window, text="请输入用户名：").pack(pady=10)
        entry = tk.Entry(window, width=30)
        entry.pack()

        def do_query():
            username = entry.get().strip()
            if username:
                books = user_service.get_user_borrowed(username)
                if books:
                    info = "\n".join([f"编号: {b[0]}, 书名: {b[1]}, 到期: {b[2]}" for b in books])
                    messagebox.showinfo("借阅信息", info)
                else:
                    messagebox.showinfo("借阅信息", "暂无借阅记录")
            else:
                messagebox.showwarning("输入错误", "请输入用户名")

        tk.Button(window, text="查询", command=do_query).pack(pady=10)


# 单独运行界面
if __name__ == "__main__":
    root = tk.Tk()
    app = UserGUI(root)
    root.mainloop()
