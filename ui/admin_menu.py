import tkinter as tk
from tkinter import messagebox
from ui.admin_gui import AdminGUI

def open_admin_menu():
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()

if __name__ == "__main__":
    open_admin_menu()