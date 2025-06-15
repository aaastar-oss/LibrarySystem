import tkinter as tk
from tkinter import messagebox
from services import user_service
import traceback

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.BG_COLOR)
        self.controller = controller
        
        # 主卡片容器
        self.card = tk.Frame(
            self,
            bg=controller.CARD_BG,
            bd=0,
            highlightthickness=0,
            relief="flat",
            padx=30,
            pady=30
        )
        self.card.pack(fill="both", expand=True, padx=40, pady=40)
        
        # 标题
        self.title_label = tk.Label(
            self.card,
            text="个人信息中心",
            font=("Microsoft YaHei", 18, "bold"),
            fg=controller.TEXT_DARK,
            bg=controller.CARD_BG
        )
        self.title_label.pack(pady=(0, 20))
        
        # 用户信息卡片
        self.info_card = tk.Frame(
            self.card,
            bg="#f8f9fa",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=20,
            pady=20
        )
        self.info_card.pack(fill="x")
        
        # 刷新按钮
        self.refresh_btn = tk.Button(
            self.card,
            text="刷新信息",
            command=self.update_data,
            font=("Microsoft YaHei", 10),
            bg=controller.PRIMARY_COLOR,
            fg="white",
            relief="flat",
            padx=15,
            pady=5
        )
        self.refresh_btn.pack(pady=10)
        
        # 初始加载用户信息
        self._load_user_info()

    def _load_user_info(self):
        """加载并显示用户信息 - 增强版"""
        print("\n[MenuPage] 开始加载用户信息")
        
        try:
            # 验证控制器和用户名
            if not hasattr(self.controller, 'username'):
                raise AttributeError("控制器缺少username属性")
            
            username = self.controller.username
            if not username:
                raise ValueError("用户名为空")
            
            print(f"[MenuPage] 正在查询用户: {username}")
            
            # 获取用户信息
            user_info = user_service.get_user_info(username)
            if not user_info:
                raise ValueError("未获取到用户信息")
            
            self._display_user_info(user_info)
            
        except AttributeError as e:
            self._handle_error(f"系统接口错误: {str(e)}", traceback.format_exc())
        except ValueError as e:
            self._handle_error(f"数据错误: {str(e)}", traceback.format_exc())
        except Exception as e:
            self._handle_error(f"系统错误: {str(e)}", traceback.format_exc())

    def _display_user_info(self, user_info):
        """显示用户信息"""
        # 清除旧信息
        for widget in self.info_card.winfo_children():
            widget.destroy()
        
        # 用户信息项配置
        info_items = [
            ("👤 用户名", user_info.get('username', 'N/A')),
            ("🔑 角色", user_info.get('role', '未知').capitalize()),
            ("📱 电话", user_info.get('phone', '未设置')),
            ("✉️ 邮箱", user_info.get('email', '未设置')),
            ("📚 借阅状态", f"{user_info.get('current_borrowed', 0)}/{user_info.get('max_borrow', 5)}"),
            ("⏳ 注册时间", user_info.get('register_time', '未知'))
        ]
        
        # 创建信息显示行
        for label, value in info_items:
            row_frame = tk.Frame(self.info_card, bg="#f8f9fa")
            row_frame.pack(fill="x", pady=5)
            
            tk.Label(
                row_frame,
                text=label,
                font=("Microsoft YaHei", 11, "bold"),
                fg="#333333",
                bg="#f8f9fa",
                width=10,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                row_frame,
                text=value,
                font=("Microsoft YaHei", 11),
                fg="#555555",
                bg="#f8f9fa",
                anchor="w"
            ).pack(side="left", padx=10)
        
        print("[MenuPage] 用户信息显示完成")
        
        # 更新状态栏
        if hasattr(self.controller, 'set_status'):
            self.controller.set_status("个人信息加载成功", self.controller.SUCCESS_COLOR)

    def _handle_error(self, message, traceback_str=None):
        """统一处理错误"""
        print(f"[ERROR] {message}")
        if traceback_str:
            print(f"[DEBUG] 错误详情:\n{traceback_str}")
        
        # 显示错误信息
        self._show_error_message(message)
        
        # 更新状态栏
        if hasattr(self.controller, 'set_status'):
            self.controller.set_status(message, self.controller.DANGER_COLOR)

    def _show_error_message(self, message):
        """显示错误信息"""
        # 清除旧内容
        for widget in self.info_card.winfo_children():
            widget.destroy()
        
        # 显示错误标签
        error_label = tk.Label(
            self.info_card,
            text=message,
            font=("Microsoft YaHei", 11),
            fg="#dc3545",
            bg="#f8f9fa",
            wraplength=350
        )
        error_label.pack()
        
        # 添加重试按钮
        retry_btn = tk.Button(
            self.info_card,
            text="重试",
            command=self.update_data,
            font=("Microsoft YaHei", 10),
            bg=self.controller.SECONDARY_COLOR,
            fg="white",
            relief="flat",
            padx=10
        )
        retry_btn.pack(pady=10)

    def update_data(self):
        """刷新数据"""
        print("[MenuPage] 刷新用户信息")
        self._load_user_info()

    def destroy(self):
        """清理资源"""
        print("[MenuPage] 清理资源")
        super().destroy()