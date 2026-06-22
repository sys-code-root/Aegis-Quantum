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
            'cryptography': 'File encryption (Ransomware).',
            'importlib': 'Dynamic module loading (Anti-Analysis bypass).'
        }

    def scan(self, file_path):
        """Parses the file into an AST and inspects import and function nodes."""
        if not os.path.exists(file_path):
            print(f"[-] Error: File {file_path} not found.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read())

            print(f"[!] Scanning: {file_path}")
            print("-" * 50)

            # Uses a set to prevent duplicate alerts in the terminal output
            detected_libs = set()

            for node in ast.walk(tree):
                # Case 1: Standard imports (e.g., 'import os')
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base_module = alias.name.split('.')[0]
                        if base_module in self.watchlist:
                            detected_libs.add(base_module)

                # Case 2: From imports (e.g., 'from socket import socket')
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base_module = node.module.split('.')[0]
                        if base_module in self.watchlist:
                            detected_libs.add(base_module)

                # Case 3: Hidden dynamic calls (e.g., '__import__("os")')
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == '__import__':
                        # Verify if the first argument passed to the function is a constant string
                        if node.args and isinstance(node.args[0], ast.Constant):
                            base_module = str(node.args[0].value).split('.')[0]
                            if base_module in self.watchlist:
                                detected_libs.add(base_module)

            # Displays the consolidated triage report
            if detected_libs:
                for lib in detected_libs:
                    self._print_alert(lib)
            else:
                print("[+] Scan completed: No suspicious core imports identified.")

        except SyntaxError:
            print("[-] Error: Target is not a valid Python script.")
        except Exception as e:
            print(f"[-] Unexpected error: {e}")

    def _print_alert(self, lib_name):
        """Prints a standardized alert block for detected libraries."""
        print(f"[!] ALERT: Suspicious import '{lib_name}' detected.")
        print(f"    Risk: {self.watchlist[lib_name]}")
        print("-" * 50)

if __name__ == "__main__":
    target = input("Enter path to target .py file: ")
    scanner = SuspiciousImportScanner()
    scanner.scan(target)
