

import tkinter as tk
from tkinter import messagebox
from ui.admin_menu import open_admin_menu
from ui.user_menu import open_user_menu

def main():
    root = tk.Tk()
    root.title("图书管理系统")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="欢迎使用图书管理系统", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=40)

    tk.Button(root, text="管理员登录", width=20, height=2, font=("Helvetica", 14),
              command=lambda: [root.destroy(), open_admin_menu()],
              bg="#4a90e2", fg="white").pack(pady=10)

    tk.Button(root, text="用户登录", width=20, height=2, font=("Helvetica", 14),
              command=lambda: [root.destroy(), open_user_menu()],
              bg="#50b674", fg="white").pack(pady=10)

    tk.Button(root, text="退出", width=20, height=2, font=("Helvetica", 14),
              command=root.quit,
              bg="#999999", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
