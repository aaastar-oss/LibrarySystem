import tkinter as tk
from tkinter import ttk
from services import user_service
import traceback

class SearchBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        
        # 主卡片容器
        card = tk.Frame(
            self,
            bg=controller.CARD_BG,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=30,
            pady=30
        )
        card.pack(fill="both", expand=True, padx=40, pady=40)
        
        # 标题区域
        title_frame = tk.Frame(card, bg=controller.CARD_BG)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="图书查询",
            font=("Microsoft YaHei", 18, "bold"),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg=controller.BORDER_COLOR)
        separator.pack(fill="x", pady=(0, 25))

        # 搜索框区域
        search_frame = tk.Frame(card, bg=controller.CARD_BG)
        search_frame.pack(fill="x", pady=(0, 15))
        
        # 搜索输入框
        self.entry = tk.Entry(
            search_frame,
            font=("Microsoft YaHei", 12),
            bg="white",
            fg="#333333",
            relief="flat",
            bd=1,
            highlightbackground=controller.BORDER_COLOR,
            highlightthickness=1,
            highlightcolor=controller.PRIMARY_COLOR,
            insertbackground=controller.PRIMARY_COLOR
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        
        # 搜索按钮
        search_btn = tk.Button(
            search_frame,
            text="查询",
            command=self.search_book,
            font=("Microsoft YaHei", 12),
            bg=controller.PRIMARY_COLOR,
            fg="white",
            activebackground="#3a56b0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=5
        )
        search_btn.pack(side="right", padx=(10, 0))
        
        # 按钮悬停效果
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#3a56b0"))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg=controller.PRIMARY_COLOR))
        
        # 结果展示区域
        result_frame = tk.Frame(card, bg=controller.CARD_BG)
        result_frame.pack(fill="both", expand=True)
        
        # 使用Treeview展示结果
        self.tree = ttk.Treeview(
            result_frame,
            columns=("编号", "书名", "作者", "出版社", "价格", "剩余"),
            show="headings",
            height=10
        )
        
        # 配置列
        columns = {
            "编号": {"width": 80, "anchor": "center"},
            "书名": {"width": 150, "anchor": "w"},
            "作者": {"width": 100, "anchor": "w"},
            "出版社": {"width": 120, "anchor": "w"},
            "价格": {"width": 80, "anchor": "e"},
            "剩余": {"width": 60, "anchor": "center"}
        }
        
        for col, config in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **config)
        
        # 添加滚动条
        scroll_y = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)
        
        scroll_x = ttk.Scrollbar(result_frame, orient="horizontal", command=self.tree.xview)
        scroll_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scroll_x.set)
        
        self.tree.pack(fill="both", expand=True)
        
        # 状态标签
        self.status_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg=controller.TEXT_LIGHT,
            bg=controller.CARD_BG,
            wraplength=500
        )
        self.status_label.pack(pady=(10, 0))
        
        # 按钮区域
        button_frame = tk.Frame(card, bg=controller.CARD_BG)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # 返回按钮
        back_btn = tk.Button(
            button_frame,
            text="返回菜单",
            command=lambda: controller.show_frame("MenuPage"),
            font=("Microsoft YaHei", 11),
            bg=controller.SECONDARY_COLOR,
            fg="white",
            activebackground="#5a6268",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        back_btn.pack(side="right")
        
        # 按钮悬停效果
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=controller.SECONDARY_COLOR))
        
        # 绑定回车键
        self.entry.bind("<Return>", lambda e: self.search_book())
        
        # 自动聚焦输入框
        self.entry.focus_set()

    def search_book(self):
        """执行图书查询"""
        keyword = self.entry.get().strip()
        
        # 清除现有数据
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # 输入验证
        if not keyword:
            self.status_label.config(
                text="请输入图书编号或书名",
                fg=self.controller.DANGER_COLOR
            )
            self.controller.set_status("查询失败：未输入关键词", color=self.controller.DANGER_COLOR)
            return
        
        try:
            # 调用服务层
            books = user_service.search_book(keyword)
            
            if books:
                for book in books:
                    self.tree.insert("", tk.END, values=(
                        book.get("id", ""),
                        book.get("title", ""),
                        book.get("author", ""),
                        book.get("publisher", ""),
                        f"￥{book.get('price', 0):.2f}",
                        book.get("available_copies", 0)
                    ))
                
                status_msg = f"找到 {len(books)} 条匹配结果"
                self.status_label.config(
                    text=status_msg,
                    fg=self.controller.SUCCESS_COLOR
                )
                self.controller.set_status(status_msg, color=self.controller.SUCCESS_COLOR)
            else:
                status_msg = "未找到匹配的图书"
                self.status_label.config(
                    text=status_msg,
                    fg=self.controller.TEXT_LIGHT
                )
                self.controller.set_status(status_msg, color=self.controller.TEXT_LIGHT)
                
        except Exception as e:
            error_msg = f"查询图书信息出错：{str(e)}"
            self.status_label.config(
                text=error_msg,
                fg=self.controller.DANGER_COLOR
            )
            self.controller.set_status(error_msg, color=self.controller.DANGER_COLOR)
            print(f"详细错误：{traceback.format_exc()}")