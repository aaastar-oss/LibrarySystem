import tkinter as tk
from tkinter import messagebox
from ui.user_gui import UserGUI

def open_user_menu():
    root = tk.Tk()
    app = UserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    open_user_menu()
