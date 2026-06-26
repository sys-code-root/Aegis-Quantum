# Email Hunter & OSINT Harvester (Project 031)

A professional reconnaissance utility engineered to automate the discovery of exposed contact artifacts (e-mail addresses). This tool facilitates efficient mapping of communication vectors, critical for security audits and surface-area triage.

## Technical Explanation

* **Heuristic Pattern Recognition:** Utilizes optimized Regular Expressions (Regex) to scan unstructured DOM or plain-text blocks. This allows the tool to ignore HTML "noise" and extract only the strings that strictly conform to standard RFC 5322 e-mail conventions.
* **Request Header Obfuscation:** Implements custom `User-Agent` headers. This simulates standard browser behavior, reducing the likelihood of the tool being flagged or blocked by WAFs (Web Application Firewalls) or simple server-side bot-detectors.
* **Memory-Efficient Deduplication:** Employs Python `set` structures as the primary storage container. Because sets are implemented as hash tables, this provides O(1) complexity for deduplication, ensuring that even if a site repeats a contact hundreds of times, the output remains clean and normalized.

## Problems Solved

* **Attack Surface Triage:** Enables security teams to rapidly identify what contact information is publicly visible, allowing organizations to obfuscate or remove sensitive addresses to reduce spam and targeted phishing.
* **Communication Vector Mapping:** Aggregates contact intelligence across vast datasets, allowing security researchers to verify site ownership or conduct audits on organizational communication hierarchies.
* **Data Normalization:** Solving the issue of "noisy data" by automatically stripping duplicates and formatting output into structured, actionable intelligence lists.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Logic** | `re` (Regex) Module | Provides high-speed, compiled pattern matching. It is significantly faster than manual string iteration for finding specific patterns. |
| **Identity** | `User-Agent` Headers | Essential for successful reconnaissance. Without a browser-like string, many servers automatically reject requests as "suspicious bot traffic." |
| **Data Storage** | `set()` Structure | Native deduplication. It ensures that every email identified is unique, saving time during the subsequent investigation or outreach phase. |
| **Performance** | Non-Persistent I/O | Operates in-memory to keep the tool ephemeral; it provides reconnaissance findings without leaving a trace of database files on the host machine. |

## Usage

This utility is designed to be the primary reconnaissance module for your OSINT pipeline. Ensure the file is saved as `email_hunter.py`.

```python
from email_hunter import EmailHunter

# 1. Initiate reconnaissance on a target organizational site
# The tool automatically manages headers and connection state
target = "[https://example.com/contact](https://example.com/contact)"
hunter = EmailHunter(target)

# 2. Execute harvester sweep and return unique contacts
contacts = hunter.hunt()

print(f"Discovered {len(contacts)} unique artifacts:")
for email in contacts:
    print(f"[+] {email}")
