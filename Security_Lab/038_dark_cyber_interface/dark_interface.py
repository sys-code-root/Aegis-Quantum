import tkinter as tk
from tkinter import messagebox

class DarkCyberInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Auditor UI Pro")
        self.root.geometry("400x300")

        self.bg_color = "#121212"
        self.fg_color = "#00ff00"
        self.root.configure(bg=self.bg_color)

        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Scan Routine", command=self.new_scan)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Terminate Console", command=self.root.quit)
        self.menu_bar.add_cascade(label="Operations", menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="System Core Specs", command=self.show_about)
        self.menu_bar.add_cascade(label="Intelligence", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

        self.lbl_status = tk.Label(
            self.root,
            text="CORE ENGINE: STANDBY",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Consolas", 12, "bold")
        )
        self.lbl_status.pack(expand=True)

    def new_scan(self):
        print("[*] Flushing memory registers for new scanning deployment context...")

    def show_about(self):
        messagebox.showinfo("System Info", "Cyber Auditor Platform\nSecurity Operations Center\nVersion 2.0")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DarkCyberInterface()
    app.run()
