import sys
import re
from datetime import datetime
from pathlib import Path
import pdfplumber
from PIL import Image

class IncidentResponseEngine:

    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.log_file = self.target_dir / "incident_response_log.txt"
        self.suspicious_pattern = re.compile(r'(\.exe$|\.bat$|\.scr$|virus|malware)', re.IGNORECASE)

    def _write_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def vaccine_logic(self, file_path):
        if self.suspicious_pattern.search(file_path.name):
            self._write_log(f"[ALERT] Vaccine: Removing {file_path.name}")
            try:
                file_path.unlink()
                return True
            except Exception as e:
                self._write_log(f"[ERROR] Failed to remove {file_path.name}: {e}")
        return False

    def sanitize_image(self, file_path):
        try:
            with Image.open(file_path) as img:
                clean_img = Image.new(img.mode, img.size)
                clean_img.paste(img)
                clean_img.save(file_path)
            self._write_log(f"[INFO] Metadata sanitized: {file_path.name}")
        except Exception as e:
            self._write_log(f"[ERROR] Failed to sanitize {file_path.name}: {e}")

    def analyze_pdf(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    if page.annots:
                        for annot in page.annots:
                            uri = annot.get('uri')
                            if uri:
                                self._write_log(f"[DANGER] Link in {file_path.name}: {uri}")
        except Exception as e:
            self._write_log(f"[ERROR] PDF Analysis failed for {file_path.name}: {e}")

    def run_full_scan(self):
        if not self.target_dir.is_dir():
            print(f"[-] Error: Target directory '{self.target_dir}' does not exist.")
            sys.exit(1)

        print(f"[*] Starting IR Engine on: {self.target_dir}")
        
        for path in self.target_dir.rglob('*'):
            if path.is_file() and path.name != self.log_file.name:
                if not self.vaccine_logic(path):
                    if path.suffix.lower() in ('.jpg', '.jpeg', '.png'):
                        self.sanitize_image(path)
                    elif path.suffix.lower() == '.pdf':
                        self.analyze_pdf(path)
                        
        print(f"[+] Scan complete. Check '{self.log_file}' for details.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ir_engine.py <target_directory>")
        sys.exit(1)

    engine = IncidentResponseEngine(sys.argv[1])
    engine.run_full_scan()
