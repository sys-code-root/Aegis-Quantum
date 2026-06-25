# Vault Intelligence Reader (Project 033)

A forensic-grade data retrieval interface engineered to empower security operators to query, filter, and review stored intelligence artifacts within the Security Lab's vault with minimal latency.

## Technical Explanation

* **Chronological Triage Indexing:** Implements `ORDER BY id DESC` as a standard retrieval protocol. This ensures that the most recent security telemetry and OSINT observations are presented first, accelerating the triage process for incident responders.
* **Fuzzy Pattern Matching:** Leverages the SQL `LIKE` operator with wildcard patterns (`%`). This enables flexible, high-speed searching across URL targets, allowing for "partial-match" discovery—crucial when the operator has only fragments of a suspicious domain.
* **Injection-Proof Retrieval:** Maintains strict adherence to parameterized SQL queries. By separating the query logic from the search input, the reader ensures that the database engine handles inputs strictly as data literals, neutralizing SQL Injection vectors during the retrieval process.

## Problems Solved

* **Intelligence Searchability:** Transmutes static database archives into a high-utility, searchable repository. This converts "data at rest" into "active intelligence" that can be navigated quickly during high-pressure investigations.
* **Contextual Retrieval:** Bridges the gap between disparate log entries. Investigators can instantly correlate artifacts related to specific domains or IPs, reconstructing the history of an entity across multiple historical scans.
* **Triage Speed:** Reduces the "Time to Insight" by ensuring that the most relevant (recent) findings are surfaced first, preventing analysts from digging through obsolete data.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Search Logic** | `LIKE` Operator | Provides efficient, engine-native pattern matching that is much faster than loading all records into Python memory and filtering with `if/else`. |
| **Retrieval Order** | `ORDER BY id DESC` | In IR (Incident Response), the latest evidence is usually the most important. Sorting by ID-descending prioritizes recent data by default. |
| **Data Integrity** | Parameterized Queries | Even in a "Read-Only" reader, parameterization is the industry standard to prevent accidental execution of malicious SQL strings. |
| **UX Strategy** | Target-Oriented Search | Focusing on "Target Domains" (URLs) aligns the tool with the operator's mental model, making it faster to use during an active investigation. |

## Usage

This utility is designed to serve as the primary retrieval interface for your forensic vault. Ensure the file is saved as `vault_reader.py`.

```python
from vault_reader import VaultReader

# 1. Connect to the intelligence vault
reader = VaultReader("lab_storage.db")

# 2. Review historical intelligence logs (Priority: Recent)
reader.list_all_scans()

# 3. Query artifacts related to a specific target domain
# This handles the wildcard search and injection protection internally
reader.search_by_url("google.com")
