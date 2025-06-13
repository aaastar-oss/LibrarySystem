import tkinter as tk
from ui.admin_menu import AdminGUI
from ui.user_menu import UserGUI

def open_admin(root):
    root.destroy()
    app = AdminGUI()
    app.mainloop()

def open_user(root):
    root.destroy()
    app = UserGUI()
    app.mainloop()

def main():
    root = tk.Tk()
    root.title("图书管理系统")
    root.geometry("400x500")
    root.configure(bg="#ffffff")

    title_font = ("微软雅黑", 24, "bold")
    btn_font = ("微软雅黑", 14)

    tk.Label(root, text="欢迎使用图书管理系统", font=title_font, bg="#ffffff", fg="#2c3e50").pack(pady=(80, 60))

    btn_config = {
        "width": 20,
        "height": 2,
        "font": btn_font,
        "bg": "#3498db",
        "fg": "white",
        "activebackground": "#2980b9",
        "activeforeground": "white",
        "relief": "flat",
        "bd": 0
    }

    tk.Button(root, text="管理员登录", command=lambda: open_admin(root), **btn_config).pack(pady=15)
    tk.Button(root, text="用户登录", command=lambda: open_user(root), **btn_config).pack(pady=15)

    exit_btn_config = btn_config.copy()
    exit_btn_config.update({
        "bg": "#95a5a6",
        "activebackground": "#7f8c8d"
    })
    tk.Button(root, text="退出", command=root.quit, **exit_btn_config).pack(pady=30)

    tk.Label(root, text="© 2025 图书管理系统", font=("微软雅黑", 10), bg="#ffffff", fg="#999999").pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
