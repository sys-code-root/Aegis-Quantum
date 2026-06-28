# Incident Response Engine (Project 010)

An automated forensic triage and cleanup engine designed to neutralize active threats, isolate malicious payloads, and sanitize digital evidence during an active incident response engagement.

## Technical Explanation

* **Deep-Recursive Traversal:** Migrated from legacy `os` logic to modern `pathlib` structures, utilizing `rglob('*')` to execute deep recursive tree scans. This ensures payloads hidden inside nested sub-directories are completely exposed.
* **Memory-Safe Image Sanitization:** Utilizes the `Pillow` library to perform high-speed binary buffer transfers (`clean_img.paste`). This modern technique instantly rebuilds the visual matrix while dropping EXIF/geolocation metadata, completely avoiding the RAM exhaustion caused by legacy pixel-by-pixel iterations.
* **Heuristic Regex Vaccination:** Upgraded naive string-matching blacklists to compiled Regular Expressions with strict end-of-line anchors (`$`). This surgical precision prevents the accidental deletion of legitimate files that share naming patterns (e.g., `report_exe.pdf`).
* **Embedded URI Extraction:** Leverages `pdfplumber` to parse the hidden annotation and structural layers of PDF documents, identifying obfuscated malicious redirect URLs masked from the naked eye.

## Problems Solved

* **Rapid Threat Containment:** Automatically identifies and purges common executable drop vectors (like rogue `.bat`, `.exe`, or `.scr` files) scattered across compromised environments.
* **Evidence OPSEC & Sanitization:** Prevents operational privacy leaks by stripping embedded metadata (creator info, timestamps, GPS coordinates) from forensic image evidence before it is shared with external analysts or legal teams.
* **Phishing Payload Discovery:** Exposes malicious Command & Control (C2) links, credential harvesting portals, or malware staging servers hidden inside seemingly benign PDF attachments.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **File I/O Traversal** | `pathlib` & `rglob` | Standard `os.listdir` creates massive forensic blind spots by ignoring sub-folders. `rglob` maps the entire architecture automatically. |
| **Image Scrubbing** | Buffer Paste vs Pixel Iteration | Extracting millions of pixels into memory crashes the host on large images. Pasting copies the visual buffer natively while dropping headers. |
| **Threat Matching** | Regex with `$` Anchors | Simple `in` string checks accidentally delete safe files containing keywords. Anchors guarantee only exact file extensions are matched. |
| **Execution Model** | CLI Target Arguments | Removes hardcoded paths, allowing IR responders to dynamically point the engine at newly mounted evidence drives directly via the terminal. |

## Usage

This tool is optimized for command-line interface (CLI) execution during fast-paced triage. Pass the compromised target directory directly as an argument:

```bash
# Execute a full IR sweep on a specific evidence folder
python ir_engine.py /mnt/evidence_drive/user_downloads
