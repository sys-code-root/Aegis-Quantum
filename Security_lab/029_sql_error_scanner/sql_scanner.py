import requests

class SQLErrorScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.sql_errors = [
            "SQL syntax", "mysql_fetch", "PostgreSQL query",
            "ORA-01756", "SQLite3::SQLException", "Driver Error"
        ]

    def scan(self):
        print(f"[*] Initiating SQLi probe on: {self.target_url}")

        payload = "'"
        test_url = self.target_url + payload

        try:
            response = requests.get(test_url, timeout=5, allow_redirects=False)

            is_vulnerable = False
            for error in self.sql_errors:
                if error.lower() in response.text.lower():
                    print(f"\n[!] VULNERABILITY IDENTIFIED: {error}")
                    print(f"[!] Target is potentially vulnerable to Error-Based SQLi.")
                    is_vulnerable = True
                    break

            if not is_vulnerable:
                print("[-] Integrity check: No database error signatures detected.")

        except Exception as e:
            print(f"[-] Connection/Probing failure: {e}")

if __name__ == "__main__":
    url = input("Enter target URL with query parameter (e.g., site.com/page.php?id=1): ")
    scanner = SQLErrorScanner(url)
    scanner.scan()
