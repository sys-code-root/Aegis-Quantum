import os
import re
from datetime import datetime

class ForensicLogParser:
    """
    Performs post-incident log forensics and automated timeline parsing.
    Scans systemic event logs to isolate indicators of compromise (IoCs) and auth faults.
    """
    def __init__(self, log_path):
        self.log_path = log_path
        self.report_file = "forensic_analysis_report.txt"
        # Security baselines indicating credential abuse, privilege escalation, or system faults
        self.suspicious_terms = [
            "FAILED", "ERROR", "DENIED", "CRITICAL", 
            "AUTH_FAILURE", "INVALID", "ROOT", "SUDO"
        ]

    def parse_logs(self):
        """Streams the target log file line-by-line to extract suspicious indicators."""
        if not os.path.exists(self.log_path):
            print(f"[-] Error: Target log artifact not found: {self.log_path}")
            return

        print(f"[*] Extracting indicators from: {self.log_path}")
        findings = []

        try:
            # errors='ignore' safely processes corrupted lines or binary junk inside text logs
            with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    upper_line = line.upper()

                    # Algorithmic signature matching across the live string block
                    if any(term in upper_line for term in self.suspicious_terms):
                        entry = f"Line {line_num}: {line.strip()}"
                        findings.append(entry)

            self.save_report(findings)
        except Exception as e:
            print(f"[-] Parsing execution breakdown: {e}")

    def save_report(self, findings):
        """Saves telemetry findings into a standardized forensic investigation report."""
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
    path = input("Enter path to target log file (e.g., /var/log/auth.log): ")
    parser = ForensicLogParser(path)
    parser.parse_logs()
