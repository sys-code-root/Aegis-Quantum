import platform
import sys
import os

class SystemIntegrityReporter:
    """
    Collects and logs basic system environment metadata.
    Useful for quick forensic environment auditing.
    """

    @staticmethod
    def get_system_info():
        """Returns a dictionary with OS, version, and architecture."""
        return {
            "OS": platform.system(),
            "Version": platform.version(),
            "Architecture": platform.machine()
        }

    @staticmethod
    def get_execution_context():
        """Checks if the script is running as a standalone binary or source."""
        # sys.frozen is set by PyInstaller when bundling the script
        return "Executable Binary" if getattr(sys, 'frozen', False) else "Standard Script"

    def generate_report(self, filename="integrity_report.log"):
        """Writes collected system data to a log file."""
        info = self.get_system_info()
        context = self.get_execution_context()

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("--- System Integrity Report ---\n")
                for key, value in info.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"Context: {context}\n")

            print(f"[+] Report generated: {os.path.abspath(filename)}")
        except IOError as e:
            print(f"[-] Failed to write report: {e}")

if __name__ == "__main__":
    reporter = SystemIntegrityReporter()
    reporter.generate_report()
