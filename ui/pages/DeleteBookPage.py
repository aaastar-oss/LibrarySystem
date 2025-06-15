import tkinter as tk
from services import admin_service

class DeleteBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 主卡片容器 - 添加阴影和更好的边距
        card = tk.Frame(
            self, 
            bg=self.controller.CARD_BG,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=30,
            pady=30
        )
        card.pack(fill="both", expand=True, padx=40, pady=40)
        
        # 标题区域 - 更突出的设计
        title_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="删除图书",
            font=("Microsoft YaHei", 18, "bold"),
            fg="#333333",
            bg=self.controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg="#e0e3e6")
        separator.pack(fill="x", pady=(0, 25))

        # 输入区域 - 更协调的布局
        input_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        input_frame.pack(fill="x", pady=20, padx=40)
        
        # 标签
        tk.Label(
            input_frame,
            text="图书编号：",
            font=("Microsoft YaHei", 12),
            fg="#555555",
            bg=self.controller.CARD_BG,
            width=8,
            anchor="e"
        ).grid(row=0, column=0, padx=8, pady=10, sticky='e')
        
        # 输入框 - 更现代的外观
        self.entry = tk.Entry(
            input_frame,
            font=("Microsoft YaHei", 12),
            bg="white",
            fg="#333333",
            relief="flat",
            bd=1,
            highlightbackground="#d1d3e2",
            highlightthickness=1,
            highlightcolor=self.controller.PRIMARY_COLOR,
            insertbackground=self.controller.PRIMARY_COLOR
        )
        self.entry.grid(row=0, column=1, padx=8, pady=10, ipady=6, sticky='ew')
        
        # 添加输入框悬停效果
        self.entry.bind("<Enter>", lambda e: self.entry.config(highlightbackground=self.controller.PRIMARY_COLOR))
        self.entry.bind("<Leave>", lambda e: self.entry.config(highlightbackground="#d1d3e2"))

        # 状态标签 - 更醒目的样式
        self.status = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg="#F44336",
            bg=self.controller.CARD_BG,
            wraplength=400
        )
        self.status.pack(pady=(15, 0))

        # 删除按钮 - 更精致的危险按钮设计
        delete_btn = tk.Button(
            card,
            text="删除图书",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.controller.DANGER_COLOR,
            fg="white",
            activebackground="#d62c1a",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.do_delete,
            padx=20,
            pady=8
        )
        delete_btn.pack(pady=(20, 10), ipady=2)
        
        # 按钮悬停效果 - 更平滑的过渡
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#d62c1a"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg=self.controller.DANGER_COLOR))

    def do_delete(self):
        book_id = self.entry.get().strip()
        if book_id:
            try:
                success = admin_service.delete_book(book_id)
                if success:
                    self.status.config(text=f"✔ 图书 {book_id} 删除成功", fg="#4CAF50")
                    self.controller.set_status(f"删除图书 {book_id} 成功", color="#4CAF50")
                    self.after(1500, self.clear_and_return)
                else:
                    self.status.config(text=f"✖ 图书 {book_id} 不存在", fg="#F44336")
                    self.controller.set_status(f"删除失败：图书 {book_id} 不存在")
            except Exception as e:
                self.status.config(text=f"✖ 删除失败：{str(e)}", fg="#F44336")
                self.controller.set_status(f"删除失败：{str(e)}")
        else:
            self.status.config(text="✖ 请输入图书编号", fg="#F44336")
            self.controller.set_status("删除失败：请输入图书编号")

    def clear_and_return(self):
        self.entry.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")