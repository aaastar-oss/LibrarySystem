import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service
from ui.pages import (
    MenuPage,
    BorrowPage,
    ReturnPage,
    AvailablePage,
    MyBooksPage,
    SearchBookPage
)
import traceback

class UserGUI(tk.Tk):
    def __init__(self, username=None):
        super().__init__()
        self.title("图书管理系统 - 用户")
        self.geometry("1200x800")
        
        # 用户名验证
        if username is None:
            raise ValueError("用户名不能为None")
        self._username = username  # 使用保护属性存储

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
        self.BTN_BG = self.PRIMARY_COLOR
        self.BTN_FG = "white"
        self.BTN_ACTIVE_BG = "#2e59d9"
        self.BTN_ACTIVE_FG = "white"
        self.ENTRY_BG = "#ffffff"
        self.BORDER_COLOR = "#d1d3e2"
        
        self.configure(bg=self.BG_COLOR)
        
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

        # 直接显示主菜单
        self.show_frame("MenuPage")

    @property
    def username(self):
        """获取用户名"""
        return self._username

    @username.setter 
    def username(self, value):
        """设置用户名"""
        if not value:
            raise ValueError("用户名不能为空")
        self._username = value
        self._update_user_display()
        
    def _update_user_display(self):
        """更新用户信息显示"""
        if hasattr(self, 'user_info_label'):
            self.user_info_label.config(text=f"当前用户：{self.username}")
        # 刷新菜单页数据
        if "MenuPage" in self.frames:
            self.frames["MenuPage"].update_data()

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
        self.frames = {}
        
        # 用户菜单页
        self.frames["MenuPage"] = MenuPage(self.content, self)
        
        # 借书页
        self.frames["BorrowPage"] = BorrowPage(self.content, self)
        
        # 还书页
        self.frames["ReturnPage"] = ReturnPage(self.content, self)
        
        # 可借图书页
        self.frames["AvailablePage"] = AvailablePage(self.content, self)
        
        # 我的图书页
        self.frames["MyBooksPage"] = MyBooksPage(self.content, self)
        
        # 图书搜索页
        self.frames["SearchBookPage"] = SearchBookPage(self.content, self)
        
        # 初始隐藏所有页面
        for name, page in self.frames.items():
            page.pack_forget()

    def _create_sidebar(self):
        """创建左侧导航栏"""
        if hasattr(self, 'sidebar') and self.sidebar:
            self.sidebar.destroy()
            
        self.sidebar = tk.Frame(self.container, bg=self.SIDEBAR_BG, width=250)
        self.sidebar.pack(side="left", fill="y")
        
        # 系统标题
        tk.Label(
            self.sidebar,
            text="图书管理系统",
            font=self.FONT_TITLE,
            bg=self.SIDEBAR_BG,
            fg="white",
            padx=50,
            pady=20
        ).pack(fill="x")
        
        # 菜单项配置
        menu_items = [
            {"header": "用户中心", "items": [("个人中心", "MenuPage")]},
            {"header": "图书操作", "items": [
                ("借阅图书", "BorrowPage"), 
                ("归还图书", "ReturnPage"),
                ("可借图书", "AvailablePage")
            ]},
            {"header": "我的信息", "items": [
                ("我的借阅", "MyBooksPage"),
                ("图书搜索", "SearchBookPage")
            ]}
        ]
        
        for section in menu_items:
            # 分类标题
            tk.Label(
                self.sidebar,
                text=section["header"],
                font=("微软雅黑", 12),
                bg=self.SIDEBAR_HEADER_BG,
                fg="white",
                pady=10,
                anchor="w"
            ).pack(fill="x", padx=10)
            
            # 菜单项
            for text, page_name in section["items"]:
                btn = tk.Label(
                    self.sidebar,
                    text=text,
                    font=self.FONT_LABEL,
                    bg=self.ACTIVE_BG if page_name == "MenuPage" else self.SIDEBAR_BG,
                    fg="white",
                    padx=20,
                    pady=10,
                    anchor="w",
                    cursor="hand2"
                )
                btn.pack(fill="x")
                
                # 绑定点击事件
                btn.bind("<Button-1>", lambda e, p=page_name: self.show_frame(p))
                
                # 悬停效果
                if page_name != "MenuPage":
                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495e"))
                    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.SIDEBAR_BG))
        
        # 用户信息区域
        self.user_info_frame = tk.Frame(self.sidebar, bg=self.SIDEBAR_HEADER_BG)
        self.user_info_frame.pack(side="bottom", fill="x", pady=10)
        
        # 用户信息标签
        self.user_info_label = tk.Label(
            self.user_info_frame,
            text=f"当前用户：{self.username}",
            font=("微软雅黑", 10),
            bg=self.SIDEBAR_HEADER_BG,
            fg="white",
            pady=15
        )
        self.user_info_label.pack(fill="x")
        
        # 返回主页按钮
        tk.Button(
            self.sidebar,
            text="返回主页",
            command=self.return_to_main,
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
            error_msg = f"错误：页面 {page_name} 不存在"
            self.set_status(error_msg, self.DANGER_COLOR)
            return
        
        # 隐藏所有页面
        for name, frame in self.frames.items():
            frame.pack_forget()
        
        # 显示目标页面
        frame = self.frames[page_name]
        
        # 如果页面有update_data方法，则调用它
        if hasattr(frame, 'update_data'):
            try:
                frame.update_data()
            except Exception as e:
                error_msg = f"刷新页面数据出错: {str(e)}"
                print(f"[ERROR] {error_msg}\n{traceback.format_exc()}")
                self.set_status(error_msg, self.DANGER_COLOR)
        
        frame.pack(fill="both", expand=True)
        self.update()

    def return_to_main(self):
        """返回主页面"""
        self.destroy()
        from main import main  # 导入主页面函数
        main()  # 重新启动主页面

    def set_status(self, message, color=None):
        """设置状态栏消息"""
        color = color or self.DANGER_COLOR
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, fg=color)

if __name__ == "__main__":
    # 测试代码 - 实际使用时应该从主页面传入真实用户名
    try:
        app = UserGUI(username="测试用户")
        app.mainloop()
    except ValueError as e:
        messagebox.showerror("初始化错误", str(e))