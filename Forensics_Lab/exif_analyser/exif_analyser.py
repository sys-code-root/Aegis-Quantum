import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class ExifAnalyser:
    
    def __init__(self, file_path):
        self.file_path = file_path

    def run_analysis(self):
        if not os.path.exists(self.file_path):
            print(f"[-] Error: File '{self.file_path}' not found.")
            return

        print(f"[!] Extracting forensic metadata: {self.file_path}")
        print("-" * 50)

        try:
            with Image.open(self.file_path) as img:
                exif_data = img.getexif()

                if not exif_data:
                    print("[!] No EXIF metadata found in this file.")
                    return

                for tag_id in exif_data:
                    tag_name = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)
                    if isinstance(data, bytes):
                        data = data.decode(errors="ignore")
                    print(f"{tag_name:<25}: {data}")

                gps_info = exif_data.get_ifd(0x8825)
                if gps_info:
                    print("\n[!] Geolocation Data (GPS Info) Identified:")
                    print("-" * 50)
                    for tag_id in gps_info:
                        tag_name = GPSTAGS.get(tag_id, tag_id)
                        data = gps_info.get(tag_id)
                        if isinstance(data, bytes):
                            data = data.decode(errors="ignore")
                        print(f"  {tag_name:<23}: {data}")

        except Exception as e:
            print(f"[-] Failed to process image archive: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exif_analyser.py <path_to_image.jpg>")
        sys.exit(1)

    analyser = ExifAnalyser(sys.argv[1])
    analyser.run_analysis()
