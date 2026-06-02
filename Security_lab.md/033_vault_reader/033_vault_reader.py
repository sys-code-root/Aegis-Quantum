import sqlite3

class VaultReader:
    """
    Provides an interface for querying and retrieving persisted security 
    intelligence artifacts from the vault database.
    """
    def __init__(self, db_name="cyber_security.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def list_all_scans(self):
        """Displays all stored intelligence artifacts in reverse chronological order."""
        print("\n--- [VAULT ARTIFACT INDEX] ---")
        query = "SELECT id, url, data_scan FROM targets ORDER BY id DESC"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        for row in rows:
            print(f"ID: {row[0]} | Target: {row[1]} | Captured: {row[2]}")

    def search_by_url(self, keyword):
        """Performs partial-match intelligence retrieval using SQL LIKE operators."""
        print(f"\n--- [SEARCH RESULTS FOR: {keyword}] ---")
        # Parameterized query protects against injection during search operations
        query = "SELECT url, emails FROM targets WHERE url LIKE ?"
        self.cursor.execute(query, ('%' + keyword + '%',))
        results = self.cursor.fetchall()

        if results:
            for res in results:
                print(f"URL:    {res[0]}\nEmails: {res[1]}\n")
        else:
            print("[-] No records identified matching the specified criteria.")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    reader = VaultReader()
    reader.list_all_scans()

    term = input("\nEnter search keyword for intelligence retrieval: ")
    reader.search_by_url(term)
    reader.close()
