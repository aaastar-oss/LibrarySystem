import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service
import traceback

class AvailablePage(tk.Frame):
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
            padx=20,
            pady=20
        )
        card.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题区域
        title_frame = tk.Frame(card, bg=controller.CARD_BG)
        title_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            title_frame,
            text="可借图书",
            font=("Microsoft YaHei", 18, "bold"),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG
        ).pack(side="left")
        
        # 添加分隔线
        separator = tk.Frame(card, height=2, bg=controller.BORDER_COLOR)
        separator.pack(fill="x", pady=(0, 15))
        
        # 控制按钮区域
        button_frame = tk.Frame(card, bg=controller.CARD_BG)
        button_frame.pack(fill="x", pady=(0, 15))
        
        # 刷新按钮
        refresh_btn = tk.Button(
            button_frame,
            text="刷新列表",
            command=self.update_data,
            font=("Microsoft YaHei", 11),
            bg=controller.SUCCESS_COLOR,
            fg="white",
            activebackground="#16a085",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        refresh_btn.pack(side="left")
        
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
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg="#16a085"))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg=controller.SUCCESS_COLOR))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=controller.SECONDARY_COLOR))
        
        # 创建Treeview表格
        self.tree_frame = tk.Frame(card, bg=controller.CARD_BG)
        self.tree_frame.pack(fill="both", expand=True)
        
        # 添加滚动条
        scroll_y = ttk.Scrollbar(self.tree_frame)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(self.tree_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        # 表格样式配置
        style = ttk.Style()
        style.configure("Treeview", 
                      font=("Microsoft YaHei", 11),
                      rowheight=25,
                      background="#ffffff",
                      fieldbackground="#ffffff",
                      foreground="#333333")
        style.configure("Treeview.Heading", 
                      font=("Microsoft YaHei", 12, "bold"),
                      background="#e0e3e6",
                      foreground="#333333")
        style.map("Treeview", 
                background=[("selected", "#e0e3e6")],
                foreground=[("selected", "#333333")])
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("编号", "书名", "作者", "出版社", "剩余数量"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        self.tree.pack(fill="both", expand=True)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # 配置列
        columns = {
            "编号": {"width": 100, "anchor": "center"},
            "书名": {"width": 200, "anchor": "w"},
            "作者": {"width": 120, "anchor": "w"},
            "出版社": {"width": 150, "anchor": "w"},
            "剩余数量": {"width": 80, "anchor": "center"}
        }
        
        for col, config in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **config)
        
        # 状态标签
        self.status_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg=controller.DANGER_COLOR,
            bg=controller.CARD_BG,
            wraplength=500
        )
        self.status_label.pack(pady=(10, 0))
        
        # 初始加载数据
        self.update_data()

    def update_data(self):
        """更新表格数据"""
        # 清除现有数据
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            books = user_service.query_books()
            if books:
                for book in books:
                    self.tree.insert("", tk.END, values=(
                        book.get("id", ""),
                        book.get("title", ""),
                        book.get("author", ""),
                        book.get("publisher", ""),
                        book.get("available_copies", 0)
                    ))
                self.status_label.config(
                    text=f"共找到 {len(books)} 本可借图书",
                    fg=self.controller.SUCCESS_COLOR
                )
                self.controller.set_status("可借图书列表已更新", color=self.controller.SUCCESS_COLOR)
            else:
                self.status_label.config(
                    text="当前没有可借图书",
                    fg=self.controller.TEXT_LIGHT
                )
                self.controller.set_status("没有可借图书", color=self.controller.TEXT_LIGHT)
        except Exception as e:
            error_msg = f"加载图书数据时出错：{str(e)}"
            self.status_label.config(
                text=error_msg,
                fg=self.controller.DANGER_COLOR
            )
            self.controller.set_status(error_msg, color=self.controller.DANGER_COLOR)
            print(f"详细错误：{traceback.format_exc()}")