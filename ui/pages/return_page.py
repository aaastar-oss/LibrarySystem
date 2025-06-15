import tkinter as tk
from tkinter import ttk
from services import user_service
import traceback

class ReturnPage(tk.Frame):
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
            text="图书归还",
            font=("Microsoft YaHei", 18, "bold"),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG
        ).pack(side="left")
        
        # 添加装饰性分隔线
        separator = tk.Frame(card, height=2, bg=controller.BORDER_COLOR)
        separator.pack(fill="x", pady=(0, 25))

        # 表单容器
        form_frame = tk.Frame(card, bg=controller.CARD_BG)
        form_frame.pack(fill="both", expand=True)
        
        # 图书编号输入
        tk.Label(
            form_frame,
            text="图书编号：",
            font=("Microsoft YaHei", 12),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.book_id_entry = tk.Entry(
            form_frame,
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
        self.book_id_entry.pack(fill="x", ipady=6)
        
        # 按钮区域
        button_frame = tk.Frame(card, bg=controller.CARD_BG)
        button_frame.pack(fill="x", pady=(20, 0))
        
        # 归还按钮
        return_btn = tk.Button(
            button_frame,
            text="确认归还",
            command=self.do_return,
            font=("Microsoft YaHei", 12, "bold"),
            bg=controller.SUCCESS_COLOR,
            fg="white",
            activebackground="#16a085",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8
        )
        return_btn.pack(pady=10, ipady=2)
        
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
        back_btn.pack(pady=(5, 0))
        
        # 按钮悬停效果
        return_btn.bind("<Enter>", lambda e: return_btn.config(bg="#16a085"))
        return_btn.bind("<Leave>", lambda e: return_btn.config(bg=controller.SUCCESS_COLOR))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#5a6268"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=controller.SECONDARY_COLOR))
        
        # 状态标签
        self.status_label = tk.Label(
            card,
            text="",
            font=("Microsoft YaHei", 11),
            fg=controller.DANGER_COLOR,
            bg=controller.CARD_BG,
            wraplength=400
        )
        self.status_label.pack(pady=(15, 0))
        
        # 绑定回车键
        self.book_id_entry.bind("<Return>", lambda e: self.do_return())
        
        # 自动聚焦输入框
        self.book_id_entry.focus_set()

    def do_return(self):
        """执行还书操作"""
        book_id = self.book_id_entry.get().strip()
        username = self.controller.username
        
        # 输入验证
        if not book_id:
            self.status_label.config(text="请输入图书编号", fg=self.controller.DANGER_COLOR)
            self.controller.set_status("还书失败：未输入编号", color=self.controller.DANGER_COLOR)
            return
            
        if not book_id.isdigit():
            self.status_label.config(text="图书编号必须是数字", fg=self.controller.DANGER_COLOR)
            self.controller.set_status("还书失败：编号格式错误", color=self.controller.DANGER_COLOR)
            return
        
        try:
            # 调用服务层
            success = user_service.return_book(username, book_id)
            
            if success:
                success_msg = "还书成功"
                self.status_label.config(text=f"✓ {success_msg}", fg=self.controller.SUCCESS_COLOR)
                self.controller.set_status(success_msg, color=self.controller.SUCCESS_COLOR)
                self.book_id_entry.delete(0, tk.END)
                
                # 3秒后清除成功消息
                self.after(3000, lambda: self.status_label.config(text=""))
            else:
                error_msg = "还书失败：可能未借该书"
                self.status_label.config(text=f"✗ {error_msg}", fg=self.controller.DANGER_COLOR)
                self.controller.set_status(error_msg, color=self.controller.DANGER_COLOR)
                
        except Exception as e:
            error_msg = f"系统错误：{str(e)}"
            self.status_label.config(text=f"✗ {error_msg}", fg=self.controller.DANGER_COLOR)
            self.controller.set_status(error_msg, color=self.controller.DANGER_COLOR)
            print(f"详细错误：{traceback.format_exc()}")