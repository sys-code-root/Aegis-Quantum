import requests

class WebDirectoryHunter:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.endswith('/') else target_url + '/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Security Auditor Context)"}

    def scan(self, wordlist_path):
        print(f"[*] Initiating directory path discovery on: {self.target_url}")

        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    directory = line.strip()
                    if not directory or directory.startswith('#'):
                        continue

                    full_url = self.target_url + directory

                    try:
                        response = requests.get(full_url, headers=self.headers, timeout=3)

                        if response.status_code == 200:
                            print(f"    [EXPOSED] (200 OK):      {full_url}")
                        elif response.status_code == 403:
                            print(f"    [RESTRICTED] (403 Forbidden): {full_url}")
                    except requests.exceptions.RequestException:
                        pass

            print("\n[*] Web path auditing sweep completed.")
        except FileNotFoundError:
            print(f"[-] Error: Target verification wordlist not found at: {wordlist_path}")

if __name__ == "__main__":
    url = input("Enter target URL for auditing (e.g., http://127.0.0.1:8080): ")
    if url.startswith("http://") or url.startswith("https://"):
        hunter = WebDirectoryHunter(url)
        hunter.scan("wordlist.txt")
    else:
        print("[-] Error: Invalid format specification. Provide a complete http/https target prefix.")
