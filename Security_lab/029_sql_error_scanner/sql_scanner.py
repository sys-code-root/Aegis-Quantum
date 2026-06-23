import requests

class SQLErrorScanner:
    """
    Performs automated SQL Injection (SQLi) discovery by detecting database 
    syntax error leakage in web application HTTP responses.
    """
    def __init__(self, target_url):
        self.target_url = target_url
        # Signatures of common database driver error messages
        self.sql_errors = [
            "SQL syntax", "mysql_fetch", "PostgreSQL query",
            "ORA-01756", "SQLite3::SQLException", "Driver Error"
        ]

    def scan(self):
        """Injects syntax-breaking payloads to trigger and capture error leakage."""
        print(f"[*] Initiating SQLi probe on: {self.target_url}")

        # Payload: Basic syntax-breaking character to force database parser errors
        payload = "'" 
        test_url = self.target_url + payload

        try:
            # allow_redirects=False captures the direct response before any login-redirects
            response = requests.get(test_url, timeout=5, allow_redirects=False)

            is_vulnerable = False
            # Signature matching: scans the response body for common DB driver feedback
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
