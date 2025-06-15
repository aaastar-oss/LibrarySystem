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

class UserGUI(tk.Tk):
    def __init__(self, username=None):
        super().__init__()
        self.title("图书管理系统 - 用户")
        self.geometry("1200x800")
        
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
        self.username = username
        
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

        # 显示登录窗口（如果未提供用户名）
        if not self.username:
            self.show_login()
        else:
            self.show_frame("MenuPage")

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
            {"header": "用户中心", "items": [("主菜单", "MenuPage")]},
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
                sidebar,
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
                    sidebar,
                    text=text,
                    font=self.FONT_LABEL,
                    bg=self.ACTIVE_BG if text == "主菜单" else self.SIDEBAR_BG,
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
                if text != "主菜单":
                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495e"))
                    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.SIDEBAR_BG))
        
        # 用户信息
        user_info = tk.Label(
            sidebar,
            text=f"当前用户：{self.username if self.username else '未登录'}",
            font=("微软雅黑", 10),
            bg=self.SIDEBAR_HEADER_BG,
            fg="white",
            pady=15
        )
        user_info.pack(side="bottom", fill="x")
        
        # 登出按钮
        tk.Button(
            sidebar,
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
        for name, frame in self.frames.items():
            frame.pack_forget()
        
        # 显示目标页面
        frame = self.frames[page_name]
        if hasattr(frame, "update_data"):
            frame.update_data()
        
        frame.pack(fill="both", expand=True)
        self.update()

    def show_login(self):
        """显示登录窗口"""
        login = tk.Toplevel(self)
        login.title("用户登录")
        login.geometry("400x250")
        login.configure(bg=self.BG_COLOR)
        login.resizable(False, False)
        
        # 使登录窗口居中
        window_width = 400
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        login.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 登录表单容器
        form_frame = tk.Frame(login, bg=self.BG_COLOR)
        form_frame.pack(pady=30)
        
        # 标题
        tk.Label(
            form_frame,
            text="用户登录",
            font=self.FONT_TITLE,
            bg=self.BG_COLOR,
            fg=self.TEXT_DARK
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 用户名标签
        tk.Label(
            form_frame,
            text="用户名：",
            font=self.FONT_LABEL,
            bg=self.BG_COLOR,
            fg=self.TEXT_DARK
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        # 用户名输入框
        username_entry = tk.Entry(
            form_frame,
            font=self.FONT_LABEL,
            bg=self.ENTRY_BG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER_COLOR,
            highlightcolor=self.PRIMARY_COLOR
        )
        username_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)
        
        # 登录按钮
        login_btn = tk.Button(
            form_frame,
            text="登录",
            command=lambda: self._handle_login(login, username_entry),
            font=self.FONT_BUTTON,
            bg=self.PRIMARY_COLOR,
            fg="white",
            activebackground=self.BTN_ACTIVE_BG,
            activeforeground=self.BTN_ACTIVE_FG,
            relief="flat",
            padx=20,
            pady=5
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # 绑定回车键
        username_entry.bind("<Return>", lambda e: self._handle_login(login, username_entry))
        
        # 聚焦输入框
        username_entry.focus_set()

    def _handle_login(self, login_window, entry):
        """处理登录逻辑"""
        username = entry.get().strip()
        if not username:
            messagebox.showwarning("输入错误", "用户名不能为空", parent=login_window)
            return
        
        # 这里可以添加实际的用户验证逻辑
        self.username = username
        login_window.destroy()
        self.show_frame("MenuPage")
        
        # 更新侧边栏用户信息
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if "当前用户" in child.cget("text"):
                        child.config(text=f"当前用户：{self.username}")

    def logout(self):
        """退出登录"""
        self.username = None
        self.show_login()

    def set_status(self, message, color=None):
        """设置状态栏消息"""
        color = color or self.DANGER_COLOR
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, fg=color)

if __name__ == "__main__":
    app = UserGUI()
    app.mainloop()