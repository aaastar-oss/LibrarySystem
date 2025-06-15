import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import authenticate, register, ADMIN_SECRET_CODE
from ui.admin_menu import AdminGUI
from ui.user_menu import UserGUI
import traceback

class AuthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry("450x600")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self._center_window()
        
        # 设置窗口图标
        self._set_window_icon()
        
        self.setup_ui()
    
    def _center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def _set_window_icon(self):
        """设置窗口图标"""
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass  # 忽略图标文件不存在的错误

    def setup_ui(self):
        # 标题样式
        title_font = ("微软雅黑", 24, "bold")
        tk.Label(
            self.root, 
            text="图书管理系统", 
            font=title_font, 
            bg="#ffffff", 
            fg="#2c3e50"
        ).pack(pady=(40, 30))

        # 创建Notebook用于切换登录/注册
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('微软雅黑', 10))
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=40, pady=10)
        
        # 登录页
        self.login_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.login_frame, text="用户登录")
        self.setup_login_ui()
        
        # 注册页
        self.register_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.register_frame, text="用户注册")
        self.setup_register_ui()
        
        # 管理员注册页(隐藏)
        self.admin_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.admin_frame, text="管理员注册", state='hidden')
        self.setup_admin_ui()
        
        # 切换按钮
        switch_frame = ttk.Frame(self.root)
        switch_frame.pack(pady=10)
        
        ttk.Button(
            switch_frame, 
            text="普通用户注册", 
            command=lambda: self.notebook.select(1),
            style='TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            switch_frame, 
            text="管理员注册", 
            command=lambda: self.notebook.select(2),
            style='TButton'
        ).pack(side='left', padx=5)
        
        # 退出按钮
        exit_btn = tk.Button(
            self.root,
            text="退出系统",
            command=self.root.quit,
            width=15,
            height=1,
            font=("微软雅黑", 10),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief="flat"
        )
        exit_btn.pack(pady=20)
        
        # 版权信息
        tk.Label(
            self.root, 
            text="© 2025 图书管理系统", 
            font=("微软雅黑", 8), 
            bg="#ffffff", 
            fg="#999999"
        ).pack(side="bottom", pady=10)
    
    def setup_login_ui(self):
        """设置登录界面"""
        # 用户名输入
        ttk.Label(self.login_frame, text="用户名:").pack(pady=(10, 0))
        self.login_username = ttk.Entry(self.login_frame)
        self.login_username.pack(fill='x', padx=20, pady=5)
        
        # 密码输入
        ttk.Label(self.login_frame, text="密码:").pack(pady=(10, 0))
        self.login_password = ttk.Entry(self.login_frame, show="*")
        self.login_password.pack(fill='x', padx=20, pady=5)
        
        # 登录按钮
        login_btn = tk.Button(
            self.login_frame,
            text="登录",
            command=self.handle_login,
            width=20,
            height=1,
            font=("微软雅黑", 12),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="flat"
        )
        login_btn.pack(pady=20)
        
        # 绑定回车键
        self.login_password.bind('<Return>', lambda event: self.handle_login())
        
        # 初始聚焦用户名输入框
        self.login_username.focus_set()
    
    def setup_register_ui(self):
        """设置普通用户注册界面"""
        # 用户名输入
        ttk.Label(self.register_frame, text="用户名:").pack(pady=(5, 0))
        self.reg_username = ttk.Entry(self.register_frame)
        self.reg_username.pack(fill='x', padx=20, pady=5)
        
        # 密码输入
        ttk.Label(self.register_frame, text="密码(至少6位):").pack(pady=(5, 0))
        self.reg_password = ttk.Entry(self.register_frame, show="*")
        self.reg_password.pack(fill='x', padx=20, pady=5)
        
        # 电话输入
        ttk.Label(self.register_frame, text="电话:").pack(pady=(5, 0))
        self.reg_phone = ttk.Entry(self.register_frame)
        self.reg_phone.pack(fill='x', padx=20, pady=5)
        
        # 邮箱输入
        ttk.Label(self.register_frame, text="邮箱:").pack(pady=(5, 0))
        self.reg_email = ttk.Entry(self.register_frame)
        self.reg_email.pack(fill='x', padx=20, pady=5)
        
        # 注册按钮
        register_btn = tk.Button(
            self.register_frame,
            text="注册普通用户",
            command=self.handle_register,
            width=20,
            height=1,
            font=("微软雅黑", 12),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            relief="flat"
        )
        register_btn.pack(pady=15)
    
    def setup_admin_ui(self):
        """设置管理员注册界面"""
        # 用户名输入
        ttk.Label(self.admin_frame, text="管理员账号:").pack(pady=(5, 0))
        self.admin_username = ttk.Entry(self.admin_frame)
        self.admin_username.pack(fill='x', padx=20, pady=5)
        
        # 密码输入
        ttk.Label(self.admin_frame, text="密码(至少8位):").pack(pady=(5, 0))
        self.admin_password = ttk.Entry(self.admin_frame, show="*")
        self.admin_password.pack(fill='x', padx=20, pady=5)
        
        # 验证码输入
        ttk.Label(self.admin_frame, text=f"管理员验证码({ADMIN_SECRET_CODE}):").pack(pady=(5, 0))
        self.admin_code = ttk.Entry(self.admin_frame, show="*")
        self.admin_code.pack(fill='x', padx=20, pady=5)
        
        # 电话输入
        ttk.Label(self.admin_frame, text="联系电话:").pack(pady=(5, 0))
        self.admin_phone = ttk.Entry(self.admin_frame)
        self.admin_phone.pack(fill='x', padx=20, pady=5)
        
        # 注册按钮
        admin_btn = tk.Button(
            self.admin_frame,
            text="注册管理员",
            command=self.handle_admin_register,
            width=20,
            height=1,
            font=("微软雅黑", 12),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            relief="flat"
        )
        admin_btn.pack(pady=15)
    
    def handle_login(self):
        """处理登录逻辑"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        if not username:
            messagebox.showerror("错误", "用户名不能为空", parent=self.root)
            self.login_username.focus_set()
            return
        
        if not password:
            messagebox.showerror("错误", "密码不能为空", parent=self.root)
            self.login_password.focus_set()
            return
        
        try:
            user = authenticate(username, password)
            if not user:
                messagebox.showerror("错误", "用户名或密码错误", parent=self.root)
                self.login_password.select_range(0, tk.END)
                self.login_password.focus_set()
                return
            
            self.root.destroy()
            if user['role'] == 'admin':
                app = AdminGUI()
            else:
                app = UserGUI(username=username)  # 传递用户名到用户界面
            app.mainloop()
            
        except Exception as e:
            messagebox.showerror("错误", f"登录过程中出错: {str(e)}", parent=self.root)
            print(f"[ERROR] 登录错误: {traceback.format_exc()}")
    
    def handle_register(self):
        """处理普通用户注册"""
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        phone = self.reg_phone.get().strip()
        email = self.reg_email.get().strip()
        
        if not all([username, password, phone, email]):
            messagebox.showerror("错误", "所有字段都必须填写", parent=self.root)
            return
        
        if len(password) < 6:
            messagebox.showerror("错误", "密码长度至少6位", parent=self.root)
            self.reg_password.focus_set()
            return
        
        try:
            if register(username, password, phone, email):
                messagebox.showinfo("成功", "注册成功，请登录", parent=self.root)
                self.notebook.select(0)  # 切换到登录页
                self.login_username.delete(0, tk.END)
                self.login_username.insert(0, username)
                self.login_password.focus()
            else:
                messagebox.showerror("错误", "注册失败，用户名可能已存在", parent=self.root)
                self.reg_username.focus_set()
        except Exception as e:
            messagebox.showerror("错误", f"注册过程中出错: {str(e)}", parent=self.root)
            print(f"[ERROR] 注册错误: {traceback.format_exc()}")
    
    def handle_admin_register(self):
        """处理管理员注册"""
        username = self.admin_username.get().strip()
        password = self.admin_password.get().strip()
        code = self.admin_code.get().strip()
        phone = self.admin_phone.get().strip()
        
        if not all([username, password, code, phone]):
            messagebox.showerror("错误", "所有字段都必须填写", parent=self.root)
            return
        
        if len(password) < 8:
            messagebox.showerror("错误", "管理员密码长度至少8位", parent=self.root)
            self.admin_password.focus_set()
            return
        
        if code != ADMIN_SECRET_CODE:
            messagebox.showerror("错误", "管理员验证码错误", parent=self.root)
            self.admin_code.focus_set()
            return
        
        try:
            if register(username, password, phone, "", is_admin=True, admin_secret=code):
                messagebox.showinfo("成功", "管理员注册成功，请登录", parent=self.root)
                self.notebook.select(0)  # 切换到登录页
                self.login_username.delete(0, tk.END)
                self.login_username.insert(0, username)
                self.login_password.focus()
            else:
                messagebox.showerror("错误", "注册失败，用户名可能已存在", parent=self.root)
                self.admin_username.focus_set()
        except Exception as e:
            messagebox.showerror("错误", f"注册过程中出错: {str(e)}", parent=self.root)
            print(f"[ERROR] 管理员注册错误: {traceback.format_exc()}")

def main():
    root = tk.Tk()
    try:
        app = AuthGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("系统错误", f"应用程序启动失败: {str(e)}")
        print(f"[CRITICAL] 应用程序错误: {traceback.format_exc()}")

if __name__ == "__main__":
    main()