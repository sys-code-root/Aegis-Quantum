import os
from datetime import datetime
import pdfplumber
from PIL import Image

class IncidentResponseEngine:
    """
    Automated engine for incident response: sanitizes images, 
    extracts malicious links from PDFs, and removes suspicious files.
    """
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.log_file = "incident_response_log.txt"

    def _write_log(self, message):
        """Appends activity with timestamp for audit trails."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {message}\n")

    def vaccine_logic(self, filename):
        """Removes files matching suspicious patterns."""
        suspicious = [".exe", ".bat", ".scr", "virus", "malware"]
        if any(pattern in filename.lower() for pattern in suspicious):
            self._write_log(f"[ALERT] Vaccine: Removing {filename}")
            os.remove(os.path.join(self.target_dir, filename))
            return True
        return False

    def sanitize_image(self, file_path):
        """Removes EXIF metadata from images to prevent tracking."""
        try:
            with Image.open(file_path) as img:
                # Rebuild image without metadata
                data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)
                clean_img.save(file_path)
            self._write_log(f"[INFO] Metadata sanitized: {file_path}")
        except Exception as e:
            self._write_log(f"[ERROR] Failed to sanitize {file_path}: {e}")

    def analyze_pdf(self, file_path):
        """Extracts hidden links from PDFs for forensic investigation."""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    if page.annots:
                        for annot in page.annots:
                            uri = annot.get('uri')
                            if uri:
                                self._write_log(f"[DANGER] Link in {file_path}: {uri}")
        except Exception as e:
            self._write_log(f"[ERROR] PDF Analysis failed for {file_path}: {e}")

    def run_full_scan(self):
        """Executes the full IR cycle on the target directory."""
        print(f"[*] Starting IR Engine on: {self.target_dir}")
        for filename in os.listdir(self.target_dir):
            path = os.path.join(self.target_dir, filename)
            if os.path.isfile(path):
                if not self.vaccine_logic(filename):
                    if filename.lower().endswith(('.jpg', '.png')):
                        self.sanitize_image(path)
                    elif filename.lower().endswith('.pdf'):
                        self.analyze_pdf(path)
        print("[+] Scan complete. Check 'incident_response_log.txt' for details.")

if __name__ == "__main__":
    engine = IncidentResponseEngine("./my_files")
    engine.run_full_scan()
