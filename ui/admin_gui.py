import tkinter as tk
from tkinter import messagebox
from services import admin_service  # 导入业务逻辑模块


class AdminGUI:
    def __init__(self, master):
        self.master = master
        master.title("图书管理系统 - 管理员")
        master.geometry("400x600")       # 窗口稍微高一点
        master.configure(bg="#f0f0f0")

        title_label = tk.Label(master, text="管理员菜单", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(40, 30))

        buttons = [
        ("录入图书", self.add_book),
        ("删除图书", self.delete_book),
        ("修改图书信息", self.modify_book),
        ("查询图书信息和状态", self.query_book),
        ("查询用户借书状态", self.query_user),
        ("总览图书信息和状态", self.overview_books),
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



    def add_book(self):
        window = tk.Toplevel(self.master)
        window.title("录入图书")
        window.geometry("350x300")

        labels = ["编号", "书名", "作者", "出版社", "出版日期", "价格"]
        entries = []

        for i, label_text in enumerate(labels):
            tk.Label(window, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(window, width=25)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_book():
            data = [e.get().strip() for e in entries]
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
                    messagebox.showinfo("成功", "图书已成功录入！")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("错误", f"录入失败：{e}")
            else:
                messagebox.showwarning("输入不完整", "请填写所有字段！")

        tk.Button(window, text="保存", command=save_book).grid(row=len(labels), columnspan=2, pady=10)

    def delete_book(self):
        window = tk.Toplevel(self.master)
        window.title("删除图书")
        window.geometry("300x150")

        tk.Label(window, text="图书编号：").pack(pady=10)
        entry = tk.Entry(window, width=25)
        entry.pack()

        def do_delete():
            book_id = entry.get().strip()
            if book_id:
                success = admin_service.delete_book(book_id)
                if success:
                    messagebox.showinfo("成功", f"图书 {book_id} 删除成功")
                    window.destroy()
                else:
                    messagebox.showerror("失败", f"图书 {book_id} 不存在")
            else:
                messagebox.showwarning("输入错误", "请输入图书编号")

        tk.Button(window, text="删除", command=do_delete).pack(pady=10)

    def modify_book(self):
        window = tk.Toplevel(self.master)
        window.title("修改图书信息")
        window.geometry("350x300")

        tk.Label(window, text="请输入图书编号：").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        entry_id = tk.Entry(window, width=25)
        entry_id.grid(row=0, column=1, padx=10, pady=5)

        labels = ["作者", "出版社", "出版日期", "价格"]
        entries = []

        for i, label_text in enumerate(labels, start=1):
            tk.Label(window, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(window, width=25)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def do_modify():
            book_id = entry_id.get().strip()
            data = [e.get().strip() for e in entries]
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
                        messagebox.showinfo("成功", f"图书 {book_id} 信息已更新")
                        window.destroy()
                    else:
                        messagebox.showerror("失败", f"图书 {book_id} 不存在")
                except Exception as e:
                    messagebox.showerror("错误", f"修改失败：{e}")
            else:
                messagebox.showwarning("输入不完整", "请填写所有字段")

        tk.Button(window, text="修改", command=do_modify).grid(row=len(labels)+1, columnspan=2, pady=10)

    def query_book(self):
        window = tk.Toplevel(self.master)
        window.title("查询图书信息")
        window.geometry("350x200")

        tk.Label(window, text="请输入图书编号或书名：").pack(pady=10)
        entry = tk.Entry(window, width=30)
        entry.pack()

        def do_query():
            keyword = entry.get().strip()
            if keyword:
                result = admin_service.query_book(keyword)
                if result:
                    book_str = f"编号: {result[0]}\n书名: {result[1]}\n作者: {result[2]}\n出版社: {result[3]}\n出版日期: {result[4]}\n价格: {result[5]}"
                    messagebox.showinfo("图书信息", book_str)
                else:
                    messagebox.showwarning("未找到", "未找到该图书")
            else:
                messagebox.showwarning("输入错误", "请输入图书编号或书名")

        tk.Button(window, text="查询", command=do_query).pack(pady=10)

    def query_user(self):
        window = tk.Toplevel(self.master)
        window.title("查询用户借阅状态")
        window.geometry("350x200")

        tk.Label(window, text="请输入用户名：").pack(pady=10)
        entry = tk.Entry(window, width=30)
        entry.pack()

        def do_query():
            username = entry.get().strip()
            if username:
                books = admin_service.query_user(username)
                if books:
                    info = "\n".join([f"编号: {b[0]}, 书名: {b[1]}, 到期: {b[2]}" for b in books])
                    messagebox.showinfo("借阅信息", info)
                else:
                    messagebox.showinfo("借阅信息", "该用户暂无借阅记录")
            else:
                messagebox.showwarning("输入错误", "请输入用户名")

        tk.Button(window, text="查询", command=do_query).pack(pady=10)

    def overview_books(self):
        books = admin_service.get_all_books()
        window = tk.Toplevel(self.master)
        window.title("图书总览")
        window.geometry("600x400")

        text = tk.Text(window, wrap='none')
        text.pack(fill='both', expand=True)

        if books:
            for b in books:
                text.insert(tk.END, f"编号:{b[0]} 书名:{b[1]} 作者:{b[2]} 出版社:{b[3]} 出版日期:{b[4]} 价格:{b[5]}\n")
        else:
            text.insert(tk.END, "暂无图书信息")


# 用于单独运行界面
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
