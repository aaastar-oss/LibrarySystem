import tkinter as tk
from services import admin_service

class AddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 主容器 - 使用更精致的卡片设计
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
            text="录入图书",
            font=("Microsoft YaHei", 18, "bold"),
            fg="#333333",
            bg=self.controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg="#e0e3e6")
        separator.pack(fill="x", pady=(0, 25))

        # 表单容器 - 更协调的布局
        form_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        form_frame.pack(fill="both", expand=True)
        
        # 表单字段配置
        fields = [
            {"label": "编号", "placeholder": ""},
            {"label": "书名", "placeholder": ""},
            {"label": "作者", "placeholder": ""},
            {"label": "出版社", "placeholder": ""},
            {"label": "出版日期", "placeholder": "YYYY-MM-DD"},
            {"label": "价格", "placeholder": "单位：元"}
        ]
        self.entries = []
        
        for i, field in enumerate(fields):
            # 标签行容器
            row_frame = tk.Frame(form_frame, bg=self.controller.CARD_BG)
            row_frame.grid(row=i, column=0, sticky="ew", pady=8)
            
            # 标签
            tk.Label(
                row_frame,
                text=field["label"],
                font=("Microsoft YaHei", 12),
                fg="#555555",
                bg=self.controller.CARD_BG,
                width=8,
                anchor="e"
            ).pack(side="left", padx=(0, 10))
            
            # 输入框
            entry = tk.Entry(
                row_frame,
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
            entry.pack(fill="x", expand=True, ipady=6)
            
            # 添加占位文本功能
            if field["placeholder"]:
                entry.insert(0, field["placeholder"])
                entry.config(fg="#999999")
                entry.bind("<FocusIn>", lambda e, w=entry, p=field["placeholder"]: 
                    self.on_entry_focus_in(w, p))
                entry.bind("<FocusOut>", lambda e, w=entry, p=field["placeholder"]: 
                    self.on_entry_focus_out(w, p))
            
            self.entries.append(entry)
        
        # 底部按钮区域
        button_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        button_frame.pack(fill="x", pady=(30, 0))
        
        # 保存按钮 - 更精致的样式
        save_btn = tk.Button(
            button_frame,
            text="保存图书",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.controller.PRIMARY_COLOR,
            fg="white",
            activebackground="#3a56b0",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.save_book,
            padx=20,
            pady=8
        )
        save_btn.pack(pady=10, ipady=2)
        
        # 按钮悬停效果
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#3a56b0"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=self.controller.PRIMARY_COLOR))
        
        # 状态标签
        self.status = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg="#F44336",
            bg=self.controller.CARD_BG,
            wraplength=400
        )
        self.status.pack(pady=(15, 0))

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#333333")

    def on_entry_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#999999")

    def save_book(self):
        data = []
        for e in self.entries:
            text = e.get().strip()
            # 忽略占位文本
            if text in ["YYYY-MM-DD", "单位：元"]:
                text = ""
            data.append(text)
            
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
                result = admin_service.add_book(book)
                if result:
                    self.status.config(text="✔ 图书已成功录入！", fg="#4CAF50")
                    self.controller.set_status("录入图书成功", color="#4CAF50")
                    self.after(1500, self.clear_and_return)
                else:
                    self.status.config(text="✖ 图书录入失败，服务未成功返回", fg="#F44336")
                    self.controller.set_status("录入图书失败，服务未成功返回")
            except ValueError:
                self.status.config(text="✖ 价格必须是数字！", fg="#F44336")
                self.controller.set_status("录入失败：价格格式错误")
            except Exception as e:
                self.status.config(text=f"✖ 录入失败：{str(e)}", fg="#F44336")
                self.controller.set_status(f"录入失败：{str(e)}")
        else:
            self.status.config(text="✖ 请填写所有字段！", fg="#F44336")
            self.controller.set_status("录入图书失败：输入不完整")

    def clear_and_return(self):
        for e in self.entries:
            e.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")