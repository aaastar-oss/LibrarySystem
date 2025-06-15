import tkinter as tk
from services import user_service

class MenuPage(tk.Frame):
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
        
        # 标题
        tk.Label(
            card,
            text="个人信息中心",
            font=("Microsoft YaHei", 18, "bold"),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG
        ).pack(pady=(0, 20))
        
        # 用户信息卡片
        self.info_card = tk.Frame(
            card,
            bg="#f8f9fa",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=20,
            pady=20
        )
        self.info_card.pack(fill="x")
        
        # 初始加载用户信息
        self._load_user_info()

    def _load_user_info(self):
        """加载并显示用户信息"""
        username = self.controller.username
        if not username:
            return
            
        try:
            # 获取用户详细信息
            user_info = user_service.get_user_info(username)
            
            # 清除旧信息
            for widget in self.info_card.winfo_children():
                widget.destroy()
            
            # 基本信息
            tk.Label(
                self.info_card,
                text=f"👤 用户名: {user_info.get('username', '')}",
                font=("Microsoft YaHei", 12),
                fg="#333333",
                bg="#f8f9fa"
            ).pack(anchor="w", pady=(0, 10))
            
            # 详细信息
            details = [
                f"🔑 角色: {user_info.get('role', '').capitalize()}",
                f"📱 电话: {user_info.get('phone', '未设置')}",
                f"✉️ 邮箱: {user_info.get('email', '未设置')}",
                f"📚 借阅状态: {user_info.get('current_borrowed', 0)}/{user_info.get('max_borrow', 5)}",
                f"⏳ 注册时间: {user_info.get('register_time', '未知')}"
            ]
            
            for detail in details:
                tk.Label(
                    self.info_card,
                    text=detail,
                    font=("Microsoft YaHei", 11),
                    fg="#555555",
                    bg="#f8f9fa"
                ).pack(anchor="w", pady=5)
                
        except Exception as e:
            tk.Label(
                self.info_card,
                text=f"加载用户信息出错: {str(e)}",
                fg="#dc3545",
                bg="#f8f9fa"
            ).pack()