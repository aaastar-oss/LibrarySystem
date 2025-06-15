import tkinter as tk
from tkinter import ttk
from services import admin_service, user_service
from ui.pages import (
    AddBookPage,
    DeleteBookPage,
    ModifyBookPage,
    QueryBookPage,
    QueryUserPage,
    OverviewBooksPage,
    MenuPage  # 导入用户中心的MenuPage
)

class AdminGUI(tk.Tk):
    def __init__(self, username="admin"):
        super().__init__()
        self.title("图书管理系统 - 管理员")
        self.geometry("1200x800")
        self._username = username  # 存储管理员用户名
        
        # UI配置变量
        self.BG_COLOR = "#f5f7fa"
        self.SIDEBAR_BG = "#2c3e50"
        self.SIDEBAR_HEADER_BG = "#34495e"
        self.ACTIVE_BG = "#3498db"
        self.CARD_BG = "#ffffff"
        self.PRIMARY_COLOR = "#4e73df"
        self.SECONDARY_COLOR = "#6c757d"
        self.SUCCESS_COLOR = "#1cc88a"
        self.DANGER_COLOR = "#e74a3b"
        self.TEXT_DARK = "#2c3e50"
        self.TEXT_LIGHT = "#7b8a8b"
        self.FONT_TITLE = ("微软雅黑", 16, "bold")
        self.FONT_LABEL = ("微软雅黑", 11)
        self.FONT_BUTTON = ("微软雅黑", 11)
        
        self.configure(bg=self.BG_COLOR)
        
        # 初始化关键属性
        self.current_active_menu = "图书总览"
        self.frames = {}
        self.menu_buttons = {}
        
        # 主容器
        self.container = tk.Frame(self, bg=self.BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        # 创建状态栏
        self._create_status_bar()
        
        # 内容区域
        self.content = tk.Frame(self.container, bg=self.BG_COLOR)
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # 初始化所有页面
        self._init_all_pages()
        
        # 创建侧边栏
        self._create_sidebar()

        # 默认显示首页
        self.show_frame("OverviewBooksPage")

    @property
    def username(self):
        """获取当前管理员用户名"""
        return self._username

    def _create_status_bar(self):
        """创建底部状态栏"""
        status_frame = tk.Frame(self, bg="#e0e6ed", height=30)
        status_frame.pack(side="bottom", fill="x")
        
        self.status_label = tk.Label(
            status_frame, 
            text="系统就绪", 
            font=("微软雅黑", 10), 
            bg="#e0e6ed", 
            fg="#666666"
        )
        self.status_label.pack(side="left", padx=10)
        
        tk.Label(
            status_frame, 
            text="© 2025 图书管理系统", 
            font=("微软雅黑", 9), 
            bg="#e0e6ed", 
            fg="#999999"
        ).pack(side="right", padx=10)

    def _init_all_pages(self):
        """初始化所有功能页面"""
        # 图书管理相关页面
        self.frames["OverviewBooksPage"] = OverviewBooksPage(self.content, self)
        self.frames["AddBookPage"] = AddBookPage(self.content, self)
        self.frames["DeleteBookPage"] = DeleteBookPage(self.content, self)
        self.frames["ModifyBookPage"] = ModifyBookPage(self.content, self)
        self.frames["QueryBookPage"] = QueryBookPage(self.content, self)
        self.frames["QueryUserPage"] = QueryUserPage(self.content, self)
        
        # 添加用户中心页面 (复用MenuPage)
        self.frames["UserCenterPage"] = MenuPage(self.content, self)
        
        # 初始隐藏所有页面
        for page in self.frames.values():
            page.pack_forget()

    def _create_sidebar(self):
        """创建左侧导航栏"""
        sidebar = tk.Frame(self.container, bg=self.SIDEBAR_BG, width=250)
        sidebar.pack(side="left", fill="y")
        
        # 系统标题
        tk.Label(
            sidebar,
            text="图书管理系统",
            font=self.FONT_TITLE,
            bg=self.SIDEBAR_BG,
            fg="white",
            padx=50,
            pady=20
        ).pack(fill="x")
        
        # 菜单项配置
        menu_items = [
            {"header": "图书管理", "items": [("图书总览", "OverviewBooksPage")]},
            {"header": "数据管理", "items": [
                ("录入图书", "AddBookPage"), 
                ("修改图书", "ModifyBookPage"),
                ("删除图书", "DeleteBookPage")
            ]},
            {"header": "查询系统", "items": [
                ("查询图书", "QueryBookPage"),
                ("用户查询", "QueryUserPage")
            ]},
            {"header": "用户中心", "items": [("个人信息", "UserCenterPage")]}  # 新增用户中心
        ]
        
        for section in menu_items:
            # 分类标题
            tk.Label(
                sidebar,
                text=section["header"],
                font=("微软雅黑", 12),
                bg=self.SIDEBAR_HEADER_BG,
                fg="white",
                pady=10,
                anchor="w"
            ).pack(fill="x", padx=10)
            
            # 创建菜单项
            for text, page_name in section["items"]:
                self._create_menu_button(sidebar, text, page_name)
        
        # 用户信息显示
        self._create_user_info_display(sidebar)

    def _create_menu_button(self, parent, text, page_name):
        """创建单个菜单按钮"""
        btn = tk.Label(
            parent,
            text=text,
            font=self.FONT_LABEL,
            bg=self.ACTIVE_BG if text == self.current_active_menu else self.SIDEBAR_BG,
            fg="white",
            padx=20,
            pady=10,
            anchor="w",
            cursor="hand2"
        )
        btn.pack(fill="x")
        self.menu_buttons[text] = btn
        
        # 绑定事件
        btn.bind("<Button-1>", lambda e, p=page_name: self.show_frame(p))
        
        if text != self.current_active_menu:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.SIDEBAR_BG))

    def _create_user_info_display(self, parent):
        """创建用户信息显示区域"""
        user_frame = tk.Frame(parent, bg=self.SIDEBAR_HEADER_BG)
        user_frame.pack(side="bottom", fill="x", pady=10)
        
        tk.Label(
            user_frame,
            text=f"当前用户：{self.username} (管理员)",
            font=("微软雅黑", 10),
            bg=self.SIDEBAR_HEADER_BG,
            fg="white",
            pady=15
        ).pack(fill="x")
        
        # 添加退出按钮
        tk.Button(
            parent,
            text="退出登录",
            command=self.logout,
            font=self.FONT_BUTTON,
            bg=self.DANGER_COLOR,
            fg="white",
            activebackground="#c0392b",
            relief="flat",
            padx=20,
            pady=5
        ).pack(side="bottom", fill="x", padx=10, pady=10)

    def show_frame(self, page_name):
        """显示指定页面"""
        if page_name not in self.frames:
            self.set_status(f"错误：页面 {page_name} 不存在", self.DANGER_COLOR)
            return
        
        # 隐藏所有页面
        for page in self.frames.values():
            page.pack_forget()
        
        # 更新菜单高亮
        self._update_menu_highlight(page_name)
        
        # 显示目标页面
        frame = self.frames[page_name]
        if hasattr(frame, "update_data"):
            frame.update_data()
        
        frame.pack(fill="both", expand=True)
        self.update()

    def _update_menu_highlight(self, page_name):
        """更新菜单高亮状态"""
        page_mapping = {
            "OverviewBooksPage": "图书总览",
            "AddBookPage": "录入图书",
            "ModifyBookPage": "修改图书",
            "DeleteBookPage": "删除图书",
            "QueryBookPage": "查询图书",
            "QueryUserPage": "用户查询",
            "UserCenterPage": "个人信息"
        }
        
        if page_name not in page_mapping:
            return
        
        new_active = page_mapping[page_name]
        
        # 清除旧高亮
        if self.current_active_menu in self.menu_buttons:
            old_btn = self.menu_buttons[self.current_active_menu]
            old_btn.config(bg=self.SIDEBAR_BG)
            old_btn.bind("<Enter>", lambda e, b=old_btn: b.config(bg="#34495e"))
            old_btn.bind("<Leave>", lambda e, b=old_btn: b.config(bg=self.SIDEBAR_BG))
        
        # 设置新高亮
        if new_active in self.menu_buttons:
            new_btn = self.menu_buttons[new_active]
            new_btn.config(bg=self.ACTIVE_BG)
            new_btn.unbind("<Enter>")
            new_btn.unbind("<Leave>")
            self.current_active_menu = new_active

    def set_status(self, message, color=None):
        """设置状态栏消息"""
        color = color or self.DANGER_COLOR
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, fg=color)

    def logout(self):
        """退出登录"""
        self.destroy()
        from main import main  # 导入主页面
        main()  # 返回登录页面

if __name__ == "__main__":
    app = AdminGUI(username="admin")  # 测试时可指定管理员用户名
    app.mainloop()