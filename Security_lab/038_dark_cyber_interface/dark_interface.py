import tkinter as tk
from tkinter import messagebox

class DarkCyberInterface:
    """
    Implements a standardized Dark Mode terminal frame interface.
    Features multi-tiered cascading menu routing controls and palette abstraction.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Auditor UI Pro")
        self.root.geometry("400x300")

        # Centralized UI Palette Definition
        self.bg_color = "#121212"
        self.fg_color = "#00ff00"
        self.root.configure(bg=self.bg_color)

        # 1. Menu Bar Subsystem Instantiation
        self.menu_bar = tk.Menu(self.root)

        # Action Cascade Menu Definition (Tearoff=0 disables detached windows)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Scan Routine", command=self.new_scan)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Terminate Console", command=self.root.quit)
        self.menu_bar.add_cascade(label="Operations", menu=self.file_menu)

        # Intelligence/Help Cascade Menu Definition
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="System Core Specs", command=self.show_about)
        self.menu_bar.add_cascade(label="Intelligence", menu=self.help_menu)

        # Injecting the configured menu component structure into the root viewport
        self.root.config(menu=self.menu_bar)

        # 2. Status Monitoring Widgets
        self.lbl_status = tk.Label(
            self.root,
            text="CORE ENGINE: STANDBY",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Consolas", 12, "bold")
        )
        self.lbl_status.pack(expand=True)

    def new_scan(self):
        """Initializes parameter setups for incoming tracking routines."""
        print("[*] Flushing memory registers for new scanning deployment context...")

    def show_about(self):
        """Triggers system meta-information dialog boxes."""
        messagebox.showinfo("System Info", "Cyber Auditor Platform\nSecurity Operations Center\nVersion 2.0")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DarkCyberInterface()
    app.run()
