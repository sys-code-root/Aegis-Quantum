# SQL Error-Based Scanner (Project 029)

A high-assurance reconnaissance utility engineered to automate the discovery of Error-Based SQL Injection (SQLi) vulnerabilities. This tool enables rapid triage of web applications by identifying server-side misconfigurations that leak database structure via verbose error messages.

## Technical Explanation

* **Payload Injection & Fuzzing:** The scanner automates the injection of syntax-breaking characters (e.g., `'`) into target URL parameters. This forces the database parser to encounter a syntax error, effectively testing if user input is being directly concatenated into the backend SQL query without parameterization.
* **Database Signature Matching:** Implements a robust signature analysis engine that scans HTTP response bodies for known database driver feedback (e.g., `SQL syntax`, `PostgreSQL query`, `SQLite3::SQLException`). This method provides a low-noise way to confirm SQLi vulnerability without relying on complex, time-consuming blind injection techniques.
* **Request Context Handling:** Utilizes `allow_redirects=False` during the probing phase. This is critical in forensic auditing as it prevents the scanner from following "Login" redirects or "Homepage" redirections, ensuring that the tool captures the *actual* server response to the injected payload.

## Problems Solved

* **Information Leakage Detection:** Immediately identifies servers that disclose structural database details (table names, column types, file paths), which are primary artifacts used by adversaries for full-scale database exploitation.
* **Input-Level Vulnerability Assessment:** Acts as a binary indicator for the lack of `Prepared Statements` or `Parameterized Queries` in the application's backend architecture.
* **Rapid Security Triage:** Enables security operators to audit hundreds of parameters in minutes, drastically reducing the "Time to Insight" before moving to more advanced testing phases.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Detection Logic** | Error-Based Analysis | It is the most deterministic method for confirming SQLi. Unlike "Blind" methods (Time/Boolean-based), Error-Based SQLi gives immediate, readable confirmation. |
| **Performance** | `requests.get` | Provides a lightweight, low-overhead way to perform probes. Since it doesn't require a browser engine, it runs extremely fast on resource-constrained forensic machines. |
| **Reliability** | Signature Matching | By using a list of known DB driver signatures, we reduce the false-positive rate. If the server says "Syntax Error near...", it is a confirmed security finding. |
| **Payload** | `'` (Single Quote) | The simplest, most effective "fuzzing" character for SQL interpreters. If the DB crashes on a single quote, it confirms an unparameterized backend query. |

## Usage

This utility is designed for the reconnaissance and discovery phase of your audit pipeline. Ensure the file is saved as `sql_scanner.py`.

```python
from sql_scanner import SQLErrorScanner

# 1. Define the target URL (must include a query parameter)
target = "[http://site-alvo.com/page.php?id=1](http://site-alvo.com/page.php?id=1)"

# 2. Initialize the scanner
scanner = SQLErrorScanner(target)

# 3. Execute the probe
# The scanner will inject payloads and output findings if a signature is hit
scanner.scan()
