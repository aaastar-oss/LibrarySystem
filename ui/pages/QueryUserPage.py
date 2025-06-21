import tkinter as tk
from tkinter import ttk
from services import admin_service

class QueryUserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 主卡片容器 - 现代化设计
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
        
        # 标题区域 - 带图标
        title_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="👤 查询用户借阅状态",
            font=("Microsoft YaHei", 18, "bold"),
            fg="#333333",
            bg=self.controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg="#e0e3e6")
        separator.pack(fill="x", pady=(0, 25))

        # 查询输入区域
        input_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        input_frame.pack(fill="x", pady=15, padx=40)
        
        # 用户名标签
        tk.Label(
            input_frame,
            text="用户名：",
            font=("Microsoft YaHei", 12),
            fg="#555555",
            bg=self.controller.CARD_BG,
            width=8,
            anchor="e"
        ).grid(row=0, column=0, padx=8, pady=10, sticky='e')
        
        # 用户名输入框
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
        
        # 输入框悬停效果
        self.entry.bind("<Enter>", lambda e: self.entry.config(highlightbackground=self.controller.PRIMARY_COLOR))
        self.entry.bind("<Leave>", lambda e: self.entry.config(highlightbackground="#d1d3e2"))

        # 查询按钮
        query_btn = tk.Button(
            input_frame,
            text="查询",
            font=("Microsoft YaHei", 12),
            bg=self.controller.PRIMARY_COLOR,
            fg="white",
            activebackground="#3a56b0",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.do_query,
            padx=20,
            pady=5
        )
        query_btn.grid(row=0, column=2, padx=(15, 0), pady=10, ipady=2)
        query_btn.bind("<Enter>", lambda e: query_btn.config(bg="#3a56b0"))
        query_btn.bind("<Leave>", lambda e: query_btn.config(bg=self.controller.PRIMARY_COLOR))

        # 表格容器
        table_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # 创建Treeview表格 - 现代化样式
        style = ttk.Style()
        style.theme_use("default")
        
        # 配置表格样式
        style.configure("Treeview",
                      background="white",
                      foreground="#333333",
                      fieldbackground="white",
                      font=("Microsoft YaHei", 11),
                      rowheight=30,
                      borderwidth=0)
        
        style.configure("Treeview.Heading",
                       font=("Microsoft YaHei", 12, "bold"),
                       background="#f8f9fa",
                       foreground="#333333",
                       padding=(10, 5),
                       borderwidth=0)
        
        style.map("Treeview", 
                 background=[("selected", self.controller.PRIMARY_COLOR)],
                 foreground=[("selected", "white")])

        # 创建借阅记录表格
        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "borrow_date"),
            show="headings",
            height=8
        )

        # 配置列
        columns = [
            ("id", "图书编号", 100),
            ("title", "书名", 200),
            ("borrow_date", "借阅日期", 150)
        ]
        
        for col_id, heading, width in columns:
            self.tree.column(col_id, width=width, anchor="center", stretch=False)
            self.tree.heading(col_id, text=heading)

        # 滚动条
        vsb = ttk.Scrollbar(
            table_frame, 
            orient="vertical", 
            command=self.tree.yview,
            style="Vertical.TScrollbar"
        )
        self.tree.configure(yscrollcommand=vsb.set)

        # 布局
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # 添加条纹行效果
        self.tree.tag_configure("oddrow", background="#f8f9fa")
        self.tree.tag_configure("evenrow", background="white")

        # 状态标签
        self.status = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg="#F44336",
            bg=self.controller.CARD_BG,
            wraplength=400
        )
        self.status.pack(pady=(10, 0))

    def do_query(self):
        username = self.entry.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not username:
            self.status.config(text="✖ 请输入用户名", fg="#F44336")
            self.controller.set_status("查询失败：请输入用户名")
            return

        books = admin_service.query_user(username)
        if books == "not_found":
            self.status.config(text="✖ 用户不存在", fg="#F44336")
            self.controller.set_status("查询失败：用户不存在")
            return
        if not books:
            self.status.config(text="✖ 该用户无借阅记录", fg="#F44336")
            self.controller.set_status("查询失败：用户无借阅记录")
            return

        for i, book in enumerate(books):
            tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
            self.tree.insert("", "end", values=(
                book.get('id', ''),
                book.get('title', ''),
                book.get('borrow_date', '')
            ), tags=tags)
        
        self.status.config(text=f"✔ 查询到 {len(books)} 条借阅记录", fg="#4CAF50")
        self.controller.set_status(f"查询到 {len(books)} 条借阅记录", color="#4CAF50")

    def update_data(self):
        self.entry.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status.config(text="")