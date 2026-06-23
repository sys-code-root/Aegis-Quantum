import sqlite3

class SecureVaultPatterns:
    def __init__(self, db_name="cyber_security.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def insecure_search(self, user_input):
        query = f"SELECT * FROM targets WHERE url = '{user_input}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def secure_search(self, user_input):
        query = "SELECT * FROM targets WHERE url = ?"
        self.cursor.execute(query, (user_input,))
        return self.cursor.fetchall()
