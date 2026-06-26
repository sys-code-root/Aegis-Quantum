import tkinter as tk

class CyberControlPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Security Lab v1.0")
        self.root.geometry("400x200")
        self.root.configure(bg="#1e1e1e")

        self.label = tk.Label(
            self.root, 
            text="OPERATIONAL SECURITY SYSTEM ACTIVE", 
            fg="#00ff00", 
            bg="#1e1e1e",
            font=("Courier", 12, "bold")
        )
        self.label.pack(pady=20)

        self.btn_exit = tk.Button(
            self.root, 
            text="SHUTDOWN CONSOLE", 
            command=self.root.quit,
            bg="#ff0000",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_exit.pack(pady=10)

    def run(self):
        print("[*] Control Panel UI thread initialized successfully.")
        self.root.mainloop()

if __name__ == "__main__":
    app = CyberControlPanel()
    app.run()
