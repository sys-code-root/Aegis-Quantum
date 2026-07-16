import tkinter as tk
from tkinter import ttk
import time

class SecurityDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Shield Operational Dashboard v1.0")
        self.root.geometry("400x350")

        self.frame_config = tk.LabelFrame(self.root, text=" Operational Parameters ", padx=10, pady=10)
        self.frame_config.pack(padx=20, pady=10, fill="both")

        self.var_stealth = tk.BooleanVar()
        self.chk_stealth = tk.Checkbutton(self.frame_config, text="Stealth Recon Mode", variable=self.var_stealth)
        self.chk_stealth.pack(anchor="w")

        self.var_log = tk.BooleanVar()
        self.chk_log = tk.Checkbutton(self.frame_config, text="Enable SQLite Forensics Log", variable=self.var_log)
        self.chk_log.pack(anchor="w")

        self.frame_action = tk.Frame(self.root, pady=20)
        self.frame_action.pack()

        self.btn_run = tk.Button(self.frame_action, text="INITIATE SECURITY SCAN", 
                                 command=self.start_progress, width=22, bg="#2c3e50", fg="white")
        self.btn_run.pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

    def start_progress(self):
        self.progress['value'] = 0
        for i in range(5):
            time.sleep(0.5) 
            self.progress['value'] += 20
            self.root.update_idletasks()
        print("[+] Operational scan pipeline finalized.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SecurityDashboard()
    app.run()
