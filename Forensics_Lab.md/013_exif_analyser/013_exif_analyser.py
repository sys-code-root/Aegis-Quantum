import os
from PIL import Image
from PIL.ExifTags import TAGS

class ExifAnalyser:
    """
    Extracts and displays EXIF metadata from image files.
    Used in digital forensics to retrieve timestamps, device info, 
    and geolocation data from image evidence.
    """
    def __init__(self, file_path="evidence.jpg"):
        self.file_path = file_path

    def run_analysis(self):
        """Processes the image and prints formatted EXIF data."""
        if not os.path.exists(self.file_path):
            print(f"[-] Error: File '{self.file_path}' not found.")
            print(f"[*] Current directory: {os.getcwd()}")
            return

        print(f"[*] Analyzing metadata for: {self.file_path}")
        print("-" * 40)

        try:
            with Image.open(self.file_path) as img:
                exif_data = img.getexif()

                if not exif_data:
                    print("[!] No EXIF metadata found in this file.")
                    return

                for tag_id in exif_data:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)

                    # Decodifica dados binários se necessário
                    if isinstance(data, bytes):
                        data = data.decode(errors="ignore")

                    print(f"{tag:<20}: {data}")

        except Exception as e:
            print(f"[-] Failed to process image: {e}")

if __name__ == "__main__":
    target = input("Enter path to image (e.g., evidence.jpg): ")
    analyser = ExifAnalyser(target)
    analyser.run_analysis()
