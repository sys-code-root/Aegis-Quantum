# Suspicious Import Scanner (Project 6)

A forensic triage tool designed to identify malicious intent in Python scripts by analyzing their structure without execution.

## Technical Explanation

* **AST Analysis:** Uses Python's native `ast` (Abstract Syntax Tree) module to parse code into its logical structure. This allows deep inspection of imports and dynamic calls without running potentially dangerous code.
* **Watchlist Heuristics:** Scans for known high-risk libraries (e.g., `socket`, `pynput`, `subprocess`) commonly used in malicious payloads and automated attacks.

## Problems Solved

* **Zero-Execution Triage:** Allows for the evaluation of scripts that could be malicious without any risk of environment infection or malware activation.
* **Obfuscation Bypass:** Identifies hidden or dynamic imports (like `__import__`) even if the code structure is complex or designed to bypass simple detection.
* **Rapid Incident Assessment:** Provides a standardized, immediate threat level estimation during the initial phase of a security incident response.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Analysis** | AST Parsing | Safer and more reliable than Regex, as it correctly identifies imports regardless of code formatting or obfuscation. |
| **Safety** | No Execution | The script reads the target file strictly as text, ensuring complete environment isolation. |
| **Structure** | Modular Class | OOP architecture designed for standalone CLI usage or seamless integration into a master security dashboard. |

## Usage

This tool is optimized for command-line interface (CLI) triage. Run the scanner by passing the target script path as an argument:

```bash
python suspicious_import_scanner.py path/to/target_script.py
