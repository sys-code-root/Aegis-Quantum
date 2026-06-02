# Suspicious Import Scanner (Project 6)

A forensic triage tool designed to identify malicious intent in Python
scripts by analyzing their structure without execution.

## Technical Explanation

-   **AST Analysis:** Uses Python\'s *ast* (Abstract Syntax Tree) module
    to parse code into its logical structure. This allows inspection of
    imports without running potentially dangerous code.
-   **Watchlist Heuristics:** Scans for known high-risk libraries (e.g.,
    *socket*, *pynput*) that are commonly used in malicious payloads.

## Problems Solved

1.  **Zero-Execution Triage:** Allows for the evaluation of scripts that
    could be malicious without risk of infection.
2.  **Obfuscation Bypass:** Identifies imports even if the code
    structure is complex or obfuscated.
3.  **Rapid Incident Assessment:** Provides an immediate threat level
    estimation during the initial phase of a security incident.

## Design Decisions: \"Why this instead of that?\"

  --------------- --------------- -----------------------------------------------------------------------------
  **Analysis**    AST Parsing     Safer than regex, as it correctly identifies imports in any code structure.
  **Safety**      No Execution    The script only reads the file as text, ensuring complete isolation.
  **Structure**   Modular Class   Designed for easy integration into the *Master_Dashboard*.
  --------------- --------------- -----------------------------------------------------------------------------

## Usage

from 006_suspicious_import_scanner import SuspiciousImportScanner\
\
scanner = SuspiciousImportScanner()\
scanner.scan(\"target_script.py\")
