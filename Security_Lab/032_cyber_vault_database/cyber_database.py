import sqlite3
from datetime import datetime

class CyberVault:
    def __init__(self, db_name="cyber_security.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_schema()

    def initialize_schema(self):
        query = """
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            emails TEXT,
            data_scan TEXT
        )
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("[+] Vault schema initialized: 'targets' table active.")

    def save_scan(self, url, email_list):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emails_str = ", ".join(email_list)

        query = "INSERT INTO targets (url, emails, data_scan) VALUES (?, ?, ?)"
        self.cursor.execute(query, (url, emails_str, timestamp))
        self.conn.commit()
        print(f"[!] Intelligence entry persisted for: {url}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    vault = CyberVault()
    vault.save_scan("http://alvo-teste.com", ["admin@teste.com", "contato@teste.com"])
    vault.close()
