import sqlite3

class DatabaseJanitor:
    def __init__(self, db_name="cyber_security.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def update_email(self, target_id, new_emails):
        query = "UPDATE targets SET emails = ? WHERE id = ?"
        self.cursor.execute(query, (new_emails, target_id))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print(f"[+] Record {target_id} successfully updated.")
        else:
            print(f"[-] Error: ID {target_id} not located in vault.")

    def delete_record(self, target_id):
        query = "DELETE FROM targets WHERE id = ?"
        self.cursor.execute(query, (target_id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            print(f"[!] Record {target_id} purged from the vault.")
        else:
            print(f"[-] Error: ID {target_id} does not exist for deletion.")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    janitor = DatabaseJanitor()
    janitor.update_email(1, "corrigido@empresa.com, admin@empresa.com")

    target_to_del = input("Enter the ID of the artifact to purge: ")
    confirm = input(f"Confirm permanent deletion of ID {target_to_del}? (s/n): ")

    if confirm.lower() == 's':
        janitor.delete_record(target_to_del)

    janitor.close()
