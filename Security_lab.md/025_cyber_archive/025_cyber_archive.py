import sqlite3
import csv
import pickle
import os

class CyberArchive:
    """
    Manages operational data persistence, reporting, and redundancy.
    Exports database states to portable CSV formats and binary pickle archives.
    """
    def __init__(self, db_name="cyber_security.db"):
        self.db_name = db_name

    def export_to_csv(self, filename="scan_report.csv"):
        """Extracts security intelligence from the database into a portable CSV layout."""
        print(f"[*] Dispatching data export to: {filename}")
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM targets")
            rows = cursor.fetchall()

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'URL', 'Emails', 'Scan_Date'])
                writer.writerows(rows)

            print(f"[+] CSV reporting layer finalized.")
        except sqlite3.Error as e:
            print(f"[-] Database extraction failure: {e}")
        finally:
            if conn: conn.close()

    def backup_objects_pickle(self, filename="vault_backup.pkl"):
        """Serializes current dataset states into a binary forensic backup object."""
        print(f"[*] Compiling binary vault backup: {filename}")
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM targets")
            data = cursor.fetchall()

            with open(filename, 'wb') as f:
                pickle.dump(data, f)

            print(f"[+] Pickle archival complete ({len(data)} serialized registry entries).")
        except Exception as e:
            print(f"[-] Archival process failure: {e}")
        finally:
            if conn: conn.close()

if __name__ == "__main__":
    archive = CyberArchive()
    archive.export_to_csv()
    archive.backup_objects_pickle()
    print("\n[✔] OPERATIONS CONCLUDED: DATABASE PERSISTED AND PROTECTED.")
