# Forensic Log Parser & Incident Auditor (Project 021)

A post-incident log forensics engine designed to parse massive system text logs line-by-line, isolating indicators of compromise (IoCs), privilege escalation attempts, and anomalous authentication mechanisms.

## Technical Explanation

* **Streaming Log Extraction:** Uses memory-safe line-by-line iterations over file descriptors, allowing the parser to process multi-gigabyte log dumps sequentially without causing RAM exhaustion.
* **Character Encoding Shielding:** Implements explicit alternative error handling (`errors='ignore'`) to prevent application crashes or stream breaks when dealing with corrupted bytes or hidden binary structures inside text lines.
* **Regex Word-Boundary Mapping:** Compiles a high-performance regular expression using word boundaries (`\b`) and case-insensitive flags. This isolates explicit security terms cleanly, preventing the false positive traps triggered by naive string intersection.

## Problems Solved

* **Brute-Force Attack Discovery:** Instantly filters out thousands of standard operational lines to isolate and group critical systemic failure events (`AUTH_FAILURE`, `DENIED`, `INVALID`).
* **Unauthorized Elevation Detection:** Flags suspicious usage or invocation of high-privilege scopes (`SUDO`, `ROOT`) to audit insider threats, lateral movements, or account takeovers.
* **Noise Reduction in Large Dumps:** Saves forensic investigators hours of manual searching by condensing massive, unstructured text logs into a clean, chronological timeline of high-risk security events.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **I/O Pattern** | Line-by-Line Stream | Far superior to `.readlines()`, which dumps the entire file into RAM and crashes the host machine when opening real enterprise log structures. |
| **Parsing Strategy** | Compiled Regex (`\b`) | Naive string containment triggers false alerts on embedded substrings (e.g., "sudoku" matching "SUDO"). Word boundaries ensure absolute alignment. |
| **Data Enforcement** | In-Place Encoding Bypass | Safely skips character conversion faults natively, maintaining processing speed and keeping timeline integrity solid without script drops. |

## Usage

This tool is optimized for command-line interface (CLI) triage operations. Run the parser by passing the target log file path directly as an argument:

```bash
python log_parser.py /var/log/auth.log
