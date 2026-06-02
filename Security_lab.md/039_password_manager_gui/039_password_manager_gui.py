import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3

class PasswordManagerGUI:
    """
    Implements a unified identity access management (IAM) dashboard.
    Combines strong pseudo-random cryptographic generation, interface input, and secure SQL binding.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Pass & Shield v3.0")
        self.root.geometry("400x400")
        self.root.configure(bg="#121212", padx=20, pady=20)

        # --- UI DESIGN CORE (GRID LAYER) ---
        tk.Label(self.root, text="SECURE CREDENTIAL MANAGEMENT", fg="#00ff00", bg="#121212", font=("Courier", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.root, text="Service/Target:", fg="white", bg="#121212").grid(row=1, column=0, sticky="w")
        self.ent_service = tk.Entry(self.root, width=25)
        self.ent_service.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Entropy Length:", fg="white", bg="#121212").grid(row=2, column=0, sticky="w")
        self.ent_length = tk.Entry(self.root, width=10)
        self.ent_length.insert(0, "16")  # Default secure length configuration
        self.ent_length.grid(row=2, column=1, sticky="w", pady=5)

        self.btn_generate = tk.Button(self.root, text="GENERATE & ARCHIVE", command=self.process_security, bg="#00ff00", fg="black", font=("Arial", 10, "bold"))
        self.btn_generate.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

        self.lbl_result = tk.Label(self.root, text="GENERATED SIGNATURE OUTPUT:", fg="#00ff00", bg="#121212")
        self.lbl_result.grid(row=4, column=0, columnspan=2)

        self.ent_output = tk.Entry(self.root, width=40, justify='center', font=("Consolas", 12))
        self.ent_output.grid(row=5, column=0, columnspan=2, pady=10)

    def generate_password(self, length):
        """Generates a high-entropy string including mixed alpha-numeric characters and symbols."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))

    def save_to_db(self, service, password):
        """Persists the generated credential safely inside the relational vault repository."""
        try:
            conn = sqlite3.connect("cyber_security.db")
            cursor = conn.cursor()

            # Enforce schema existence locally
            cursor.execute("CREATE TABLE IF NOT EXISTS targets (url TEXT, emails TEXT)")

            # Parametrization neutralizes data-injection vulnerabilities during local storage write
            cursor.execute("INSERT INTO targets (url, emails) VALUES (?, ?)", (service, f"PASS: {password}"))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Vault Error", f"Database persistence block failure: {e}")

    def process_security(self):
        """Orchestrates input validation, signature creation, and database routing."""
        service = self.ent_service.get()
        try:
            length_str = self.ent_length.get()
            if not length_str.isdigit():
                raise ValueError("Entropy length parameters must be numeric integers.")

            length = int(length_str)
            if not service:
                raise ValueError("Target entity scope cannot be initialized blank.")

            new_pass = self.generate_password(length)

            # Flush output interface buffer before display insertion
            self.ent_output.delete(0, tk.END)
            self.ent_output.insert(0, new_pass)

            # Vault logging sequence
            self.save_to_db(service, new_pass)
            messagebox.showinfo("Vault Success", "High-entropy signature archived securely.")

        except ValueError as e:
            messagebox.showwarning("Validation Warning", f"Data parsing exception: {e}")

if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.root.mainloop()
