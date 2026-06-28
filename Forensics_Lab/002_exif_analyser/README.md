# EXIF Metadata Analyser (Project 013)

A lightweight forensic tool designed to extract hidden metadata from image files.

## Technical Explanation

* **Metadata Parsing:** Uses the `Pillow` library to access the EXIF directory directly within image headers.
* **Tag Translation:** Maps numeric EXIF and Sub-IFD IDs to human-readable labels using `PIL.ExifTags` and `GPSTAGS`.
* **Robust Error Handling:** Safely handles non-text binary data, preventing crashes when reading corrupted, raw, or obfuscated metadata.

## Problems Solved

* **Device Attribution:** Identifies the exact hardware (make and model) used to capture or create the file.
* **Timeline Analysis:** Extracts the precise date and time a photo was taken, completely independent of the file's "creation/modification date" attributes on the host OS.
* **Location Discovery:** Retrieves embedded GPS coordinates (IFD structures) to trace the exact physical origin and geographical location of the image evidence.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Parsing** | `PIL.ExifTags` | Provides a standardized, fast, and native way to resolve EXIF keys without external binary dependencies. |
| **Safety** | `with` statement | Context managers guarantee that file handles are instantly released post-analysis, a critical best practice in forensic environments. |
| **Readability** | f-strings | Uses formatted alignment (`:<25`) to build professional, perfectly aligned column-based console output. |

## Usage

This tool is optimized for rapid command-line interface (CLI) triage. Run the analyser by passing the target image path as an argument:

```bash
python exif_analyser.py path/to/evidence.jpg
