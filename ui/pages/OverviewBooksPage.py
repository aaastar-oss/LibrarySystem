import tkinter as tk
from tkinter import ttk
from services import admin_service

class OverviewBooksPage(tk.Frame):
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
            text="📚 图书总览",
            font=("Microsoft YaHei", 18, "bold"),
            fg="#333333",
            bg=self.controller.CARD_BG
        ).pack(side="left")
        
        # 刷新按钮 - 更精致的样式
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 刷新数据",
            font=("Microsoft YaHei", 12),
            bg=self.controller.PRIMARY_COLOR,
            fg="white",
            activebackground="#3a56b0",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.update_data
        )
        refresh_btn.pack(side="right", padx=5)
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg="#3a56b0"))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg=self.controller.PRIMARY_COLOR))

        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg="#e0e3e6")
        separator.pack(fill="x", pady=(0, 20))

        # 表格容器
        table_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建Treeview表格 - 更现代化的样式
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

        # 创建表格
        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "author", "publisher", "publish_date", "price", "available_copies", "total_copies", "borrowed"),
            show="headings",
            height=15,
            selectmode="extended"
        )

        # 配置列
        columns = [
            ("id", "编号", 80),
            ("title", "书名", 200),
            ("author", "作者", 120),
            ("publisher", "出版社", 150),
            ("publish_date", "出版日期", 120),
            ("price", "价格", 80),
            ("available_copies", "库存", 60),
            ("total_copies", "总库存", 60),
            ("borrowed", "已借出", 60)
        ]
        
        for col_id, heading, width in columns:
            self.tree.column(col_id, width=width, anchor="center")
            self.tree.heading(col_id, text=heading)

        # 滚动条 - 更精致的样式
        vsb = ttk.Scrollbar(
            table_frame, 
            orient="vertical", 
            command=self.tree.yview,
            style="Vertical.TScrollbar"
        )
        hsb = ttk.Scrollbar(
            table_frame, 
            orient="horizontal", 
            command=self.tree.xview,
            style="Horizontal.TScrollbar"
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # 添加条纹行效果
        self.tree.tag_configure("oddrow", background="#f8f9fa")
        self.tree.tag_configure("evenrow", background="white")

        # 初始加载数据
        self.update_data()

    def update_data(self):
        """刷新表格数据"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data = admin_service.query_all_books()
        
        if data:
            for i, book in enumerate(data):
                publish_date = book.get('publish_date', '')
                if hasattr(publish_date, 'strftime'):
                    publish_date = publish_date.strftime('%Y-%m-%d')
                elif publish_date is None:
                    publish_date = ''
                try:
                    price = f"{float(book.get('price', 0)):.2f}"
                except (ValueError, TypeError):
                    price = "0.00"
                tags = ("evenrow",) if i % 2 == 0 else ("oddrow",)
                self.tree.insert("", "end", values=(
                    book.get('id', ''),
                    book.get('title', ''),
                    book.get('author', ''),
                    book.get('publisher', ''),
                    str(publish_date),
                    price,
                    book.get('available_copies', 0),
                    book.get('total_copies', 0),
                    book.get('borrowed', 0)
                ), tags=tags)
            
            self.controller.set_status(f"✔ 已加载 {len(data)} 条图书记录", color="#4CAF50")
        else:
            self.controller.set_status("✖ 无图书记录", color="#F44336")