import tkinter as tk

class CyberControlPanel:
    """
    Establishes the fundamental GUI window context and event-loop scaffolding
    for operational security applications.
    """
    def __init__(self):
        # 1. Instantiating the primary window node (Root window context)
        self.root = tk.Tk()

        # 2. Hardening and Styling the Environment Window
        self.root.title("Cyber Security Lab v1.0")
        self.root.geometry("400x200")  
        self.root.configure(bg="#1e1e1e")  # Base Dark Mode enforcement

        # 3. Constructing Static Monitoring and Interface Widgets
        self.label = tk.Label(
            self.root, 
            text="OPERATIONAL SECURITY SYSTEM ACTIVE", 
            fg="#00ff00",  # Terminal green palette
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
        """Launches the window execution thread and enters the kernel event-driven mainloop."""
        print("[*] Control Panel UI thread initialized successfully.")
        self.root.mainloop()

if __name__ == "__main__":
    app = CyberControlPanel()
    app.run()
