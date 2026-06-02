import ast
import os

class SuspiciousImportScanner:
    """
    Analyzes Python scripts for suspicious library imports without executing them.
    Used in Incident Response for rapid triage of potentially malicious scripts.
    """

    def __init__(self):
        # Watchlist of high-risk libraries for security auditing
        self.watchlist = {
            'os': 'System file manipulation.',
            'subprocess': 'Shell command execution.',
            'socket': 'Network communication (Backdoor).',
            'requests': 'Data exfiltration via HTTP.',
            'pynput': 'Keylogging capabilities.',
            'base64': 'Used for obfuscating payloads.',
            'cryptography': 'File encryption (Ransomware).'
        }

    def scan(self, file_path):
        """Parses the file into an AST and inspects import nodes."""
        if not os.path.exists(file_path):
            print(f"[-] Error: File {file_path} not found.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read())

            print(f"[!] Scanning: {file_path}")
            print("-" * 40)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._check_library(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    self._check_library(node.module)

        except SyntaxError:
            print("[-] Error: Target is not a valid Python script.")
        except Exception as e:
            print(f"[-] Unexpected error: {e}")

    def _check_library(self, lib_name):
        """Verifies if the import is on the watchlist."""
        if lib_name in self.watchlist:
            print(f"[!] ALERT: Suspicious import '{lib_name}' detected.")
            print(f"    Risk: {self.watchlist[lib_name]}")

if __name__ == "__main__":
    target = input("Enter path to target .py file: ")
    scanner = SuspiciousImportScanner()
    scanner.scan(target)
