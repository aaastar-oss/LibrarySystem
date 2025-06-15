import tkinter as tk
from services import admin_service

class ModifyBookPage(tk.Frame):
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
            text="修改图书信息",
            font=("Microsoft YaHei", 18, "bold"),
            fg="#333333",
            bg=self.controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg="#e0e3e6")
        separator.pack(fill="x", pady=(0, 25))

        # 表单容器 - 更协调的布局
        form_frame = tk.Frame(card, bg=self.controller.CARD_BG)
        form_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # 图书编号输入行
        row_frame = tk.Frame(form_frame, bg=self.controller.CARD_BG)
        row_frame.grid(row=0, column=0, sticky="ew", pady=8)
        
        tk.Label(
            row_frame,
            text="图书编号：",
            font=("Microsoft YaHei", 12),
            fg="#555555",
            bg=self.controller.CARD_BG,
            width=8,
            anchor="e"
        ).pack(side="left", padx=(0, 10))
        
        self.entry_id = tk.Entry(
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
        self.entry_id.pack(fill="x", expand=True, ipady=6)
        
        # 添加输入框悬停效果
        self.entry_id.bind("<Enter>", lambda e: self.entry_id.config(highlightbackground=self.controller.PRIMARY_COLOR))
        self.entry_id.bind("<Leave>", lambda e: self.entry_id.config(highlightbackground="#d1d3e2"))

        # 其他字段
        fields = [
            {"label": "作者", "placeholder": ""},
            {"label": "出版社", "placeholder": ""},
            {"label": "出版日期", "placeholder": "YYYY-MM-DD"},
            {"label": "价格", "placeholder": "单位：元"}
        ]
        self.entries = []
        
        for i, field in enumerate(fields, start=1):
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

        # 修改按钮 - 更精致的样式
        modify_btn = tk.Button(
            card,
            text="修改图书信息",
            font=("Microsoft YaHei", 12, "bold"),
            bg=self.controller.PRIMARY_COLOR,
            fg="white",
            activebackground="#3a56b0",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.do_modify,
            padx=20,
            pady=8
        )
        modify_btn.pack(pady=(20, 10), ipady=2)
        
        # 按钮悬停效果 - 更平滑的过渡
        modify_btn.bind("<Enter>", lambda e: modify_btn.config(bg="#3a56b0"))
        modify_btn.bind("<Leave>", lambda e: modify_btn.config(bg=self.controller.PRIMARY_COLOR))

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#333333")

    def on_entry_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#999999")

    def do_modify(self):
        book_id = self.entry_id.get().strip()
        data = []
        for e in self.entries:
            text = e.get().strip()
            # 忽略占位文本
            if text in ["YYYY-MM-DD", "单位：元"]:
                text = ""
            data.append(text)
            
        if book_id and all(data):
            try:
                new_data = {
                    "author": data[0],
                    "publisher": data[1],
                    "publish_date": data[2],
                    "price": float(data[3])
                }
                success = admin_service.modify_book(book_id, new_data)
                if success:
                    self.status.config(text=f"✔ 图书 {book_id} 信息已更新", fg="#4CAF50")
                    self.controller.set_status(f"修改图书 {book_id} 成功", color="#4CAF50")
                    self.after(1500, self.clear_and_return)
                else:
                    self.status.config(text=f"✖ 图书 {book_id} 不存在", fg="#F44336")
                    self.controller.set_status(f"修改失败：图书 {book_id} 不存在")
            except ValueError:
                self.status.config(text="✖ 价格必须是数字！", fg="#F44336")
                self.controller.set_status("修改失败：价格格式错误")
            except Exception as e:
                self.status.config(text=f"✖ 修改失败：{str(e)}", fg="#F44336")
                self.controller.set_status(f"修改失败：{str(e)}")
        else:
            self.status.config(text="✖ 请填写所有字段", fg="#F44336")
            self.controller.set_status("修改失败：输入不完整")

    def clear_and_return(self):
        self.entry_id.delete(0, tk.END)
        for e in self.entries:
            e.delete(0, tk.END)
        self.status.config(text="")
        self.controller.show_frame("MenuPage")