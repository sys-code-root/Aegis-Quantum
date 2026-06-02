import requests

class WebDirectoryHunter:
    """
    Performs active directory enumeration and web path auditing.
    Assists administrators in locating exposed endpoints or misconfigured access controls.
    """
    def __init__(self, target_url):
        # Enforce clean URL trailing slash mappings
        self.target_url = target_url if target_url.endswith('/') else target_url + '/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Security Auditor Context)"}

    def scan(self, wordlist_path):
        """Iterates through a directory wordlist to test response parameters on the host."""
        print(f"[*] Initiating directory path discovery on: {self.target_url}")

        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    directory = line.strip()
                    # Skip empty lines or commented definitions
                    if not directory or directory.startswith('#'):
                        continue

                    full_url = self.target_url + directory

                    try:
                        # Low timeout keeps validation performance optimized
                        response = requests.get(full_url, headers=self.headers, timeout=3)

                        if response.status_code == 200:
                            print(f"    [EXPOSED] (200 OK):      {full_url}")
                        elif response.status_code == 403:
                            print(f"    [RESTRICTED] (403 Forbidden): {full_url}")
                    except requests.exceptions.RequestException:
                        pass  # Bypass network drops or connection limits safely

            print("\n[*] Web path auditing sweep completed.")
        except FileNotFoundError:
            print(f"[-] Error: Target verification wordlist not found at: {wordlist_path}")

if __name__ == "__main__":
    # Standard testing parameters targeting generic structures
    url = input("Enter target URL for auditing (e.g., http://127.0.0.1:8080): ")
    if url.startswith("http://") or url.startswith("https://"):
        hunter = WebDirectoryHunter(url)
        # Expects a standard localized wordlist context
        hunter.scan("wordlist.txt")
    else:
        print("[-] Error: Invalid format specification. Provide a complete http/https target prefix.")
