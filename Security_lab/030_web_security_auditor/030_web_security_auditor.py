import requests

class SecurityHeaderAuditor:
    """
    Audits web server security posture by validating HTTP response headers
    and identifying insecure cookie configurations.
    """
    def __init__(self, url):
        self.url = url
        # Security baselines for modern web application hardening
        self.headers_to_check = [
            "X-Frame-Options", 
            "X-Content-Type-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security"
        ]

    def audit(self):
        """Performs a lightweight HEAD request to audit header security protocols."""
        print(f"[*] Initiating security posture audit for: {self.url}\n")
        try:
            # HEAD request optimizes performance by ignoring body content
            response = requests.head(self.url, timeout=5, allow_redirects=True)

            print("--- Header Hardening Analysis ---")
            for header in self.headers_to_check:
                if header in response.headers:
                    print(f"    [SAFE] {header}: Present")
                else:
                    print(f"    [VULNERABLE] {header}: MISSING")

            print("\n--- Session Cookie Analysis ---")
            if not response.cookies:
                print("    [i] No session cookies identified.")
            else:
                for cookie in response.cookies:
                    # HttpOnly prevents client-side scripts from accessing session tokens
                    is_secure = cookie.has_nonstandard_attr('HttpOnly') or 'httponly' in str(cookie).lower()
                    status = "SAFE" if is_secure else "VULNERABLE (HttpOnly flag missing)"
                    print(f"    [*] Cookie '{cookie.name}': {status}")

        except Exception as e:
            print(f"[-] Auditing execution breakdown: {e}")

if __name__ == "__main__":
    target = input("Enter target URL for security audit (e.g., https://github.com): ")
    if not target.startswith("http"):
        target = "https://" + target
    auditor = SecurityHeaderAuditor(target)
    auditor.audit()
