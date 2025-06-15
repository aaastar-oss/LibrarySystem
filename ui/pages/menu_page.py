import tkinter as tk
from services import user_service
import traceback

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller  # 保存控制器引用
        
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
        """加载并显示用户信息 - 修复版本"""
        print(f"\n[MenuPage调试] 开始加载用户信息")
        print(f"[MenuPage调试] 控制器ID: {id(self.controller)}")
        
        # 更健壮的用户名获取方式
        current_username = getattr(self.controller, 'username', None)
        print(f"[MenuPage调试] 获取到的用户名: {current_username}")
        
        if not current_username:
            print("[MenuPage调试] 用户名无效")
            self._show_error_message("未获取到用户信息")
            return
        
        try:
            print(f"[MenuPage调试] 正在查询用户信息...")
            user_info = user_service.get_user_info(current_username)
            
            if not user_info:
                print("[MenuPage调试] 查询结果为空")
                self._show_error_message("用户不存在")
                return
                
            print(f"[MenuPage调试] 获取到用户信息: {user_info}")
            self._display_user_info(user_info)
            
        except Exception as e:
            error_msg = f"加载用户信息出错: {str(e)}"
            print(f"[MenuPage调试] 发生异常: {error_msg}")
            print(f"[MenuPage调试] 详细错误：{traceback.format_exc()}")
            self._show_error_message(error_msg)

    def _display_user_info(self, user_info):
        """显示用户信息"""
        print("[MenuPage调试] 渲染用户信息")
        # 清除旧信息
        for widget in self.info_card.winfo_children():
            widget.destroy()
        
        # 显示基本信息
        info_items = [
            ("👤  用户名", user_info.get('username', 'N/A')),
            ("🔑  角色", user_info.get('role', '未知').capitalize()),
            ("📱  电话", user_info.get('phone', '未设置')),
            ("✉️ 邮箱", user_info.get('email', '未设置')),
            ("📚  借阅状态", f"{user_info.get('current_borrowed', 0)}/{user_info.get('max_borrow', 5)}"),
            ("⏳  注册时间", user_info.get('register_time', '未知'))
        ]
        
        for label, value in info_items:
            frame = tk.Frame(self.info_card, bg="#f8f9fa")
            frame.pack(fill="x", pady=5)
            
            tk.Label(
                frame,
                text=label,
                font=("Microsoft YaHei", 11, "bold"),
                fg="#333333",
                bg="#f8f9fa",
                width=10,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                frame,
                text=value,
                font=("Microsoft YaHei", 11),
                fg="#555555",
                bg="#f8f9fa",
                anchor="w"
            ).pack(side="left", padx=10)
        
        print("[MenuPage调试] 用户信息显示完成")

    def _show_error_message(self, message):
        """显示错误信息"""
        print(f"[MenuPage调试] 显示错误: {message}")
        for widget in self.info_card.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.info_card,
            text=message,
            font=("Microsoft YaHei", 11),
            fg="#dc3545",
            bg="#f8f9fa"
        ).pack()

    def update_data(self):
        """新增方法：供外部调用来刷新数据"""
        print("[MenuPage] 收到刷新请求")
        self._load_user_info()