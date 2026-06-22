import os
import re
import sys
from datetime import datetime

class ForensicLogParser:
    
    def __init__(self, log_path):
        self.log_path = log_path
        self.report_file = "forensic_analysis_report.txt"
        suspicious_terms = ["FAILED", "ERROR", "DENIED", "CRITICAL", "AUTH_FAILURE", "INVALID", "ROOT", "SUDO"]
        self.pattern = re.compile(r'\b(' + '|'.join(suspicious_terms) + r')\b', re.IGNORECASE)

    def parse_logs(self):
        if not os.path.exists(self.log_path):
            print(f"[-] Error: Target log artifact not found: {self.log_path}")
            return

        print(f"[*] Extracting indicators from: {self.log_path}")
        findings = []

        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if self.pattern.search(line):
                        findings.append(f"Line {line_num}: {line.strip()}")

            self.save_report(findings)
        except Exception as e:
            print(f"[-] Parsing execution breakdown: {e}")

    def save_report(self, findings):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.report_file, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write("          FORENSIC LOG ANALYSIS REPORT\n")
                f.write("==================================================\n")
                f.write(f"Generated on:  {timestamp}\n")
                f.write(f"Target Source: {self.log_path}\n")
                f.write("-" * 50 + "\n\n")

                if not findings:
                    f.write("[+] Security Assessment: No suspicious patterns identified.\n")
                else:
                    f.write(f"[!] Warning: Isolated {len(findings)} suspicious event entries:\n\n")
                    for item in findings:
                        f.write(f"{item}\n")

            print(f"[+] Analysis complete! {len(findings)} security events isolated.")
            print(f"[*] Forensic evidence report saved to: {self.report_file}")
        except Exception as e:
            print(f"[-] Failed to export forensic report: {e}")

    if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("Usage: python log_parser.py <path_to_log>")
            sys.exit(1)

        parser = ForensicLogParser(sys.argv[1])
        parser.parse_logs()
