import requests
import re

class EmailHunter:
    """
    Performs OSINT collection by scraping web artifacts for exposed email addresses.
    Assists in identifying potential social engineering vectors and contact intelligence.
    """
    def __init__(self, target_url):
        self.target_url = target_url
        # Standard Regex pattern to validate RFC 5322-compliant email structures
        self.email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def hunt(self):
        """Streams the target web page code to extract unique contact intelligence."""
        print(f"[*] Initiating intelligence gathering on: {self.target_url}")
        try:
            # Masking request as a standard browser agent to maintain operational transparency
            headers = {"User-Agent": "Mozilla/5.0 (Intelligence Gathering Bot)"}
            response = requests.get(self.target_url, headers=headers, timeout=10)

            # Algorithmic pattern matching to isolate email artifacts
            emails_found = re.findall(self.email_regex, response.text)

            # set() deduplication ensures clean intelligence output
            unique_emails = set(emails_found)

            if unique_emails:
                print(f"\n[+] Intelligence Success: {len(unique_emails)} unique contact artifacts identified:")
                for email in unique_emails:
                    print(f"  - {email}")
            else:
                print("[-] Intelligence Result: No contact artifacts identified on target scope.")

        except Exception as e:
            print(f"[-] Intelligence gathering fault: {e}")

if __name__ == "__main__":
    url = input("Enter target URL for OSINT contact harvesting: ")
    if not url.startswith("http"):
        url = "https://" + url

    hunter = EmailHunter(url)
    hunter.hunt()
