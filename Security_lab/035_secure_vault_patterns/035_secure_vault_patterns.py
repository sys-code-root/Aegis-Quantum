import sqlite3

class SecureVaultPatterns:
    """
    Demonstrates the difference between insecure string concatenation and 
    parameterized SQL queries to prevent SQL Injection (SQLi).
    """
    def __init__(self, db_name="cyber_security.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def insecure_search(self, user_input):
        """
        [!] VULNERABLE: Uses direct string formatting.
        The database engine executes user input as part of the SQL command.
        """
        query = f"SELECT * FROM targets WHERE url = '{user_input}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def secure_search(self, user_input):
        """
        [+] SECURE: Uses Parameterized Queries (Placeholders).
        The database treats user input strictly as a data literal, preventing command injection.
        """
        query = "SELECT * FROM targets WHERE url = ?"
        self.cursor.execute(query, (user_input,))
        return self.cursor.fetchall()
