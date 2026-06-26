# Cyber Vault Intelligence Store (Project 032)

A specialized forensic archival engine designed for the Security Lab. This component acts as the persistent storage layer, transforming transient intelligence artifacts (scan results, OSINT findings) into structured, queryable, and auditable data.

## Technical Explanation

* **Serverless Relational Persistence:** Utilizes `SQLite3` to provide a high-performance, file-based relational database. By avoiding external server daemons, the vault remains entirely portable, making it ideal for distributed forensic toolkits and air-gapped environments.
* **Defense-in-Depth Security:** Implements rigorous Parameterized Queries (`?` placeholders). This design choice ensures that all ingested data is treated strictly as value-literals, fundamentally neutralizing SQL Injection vectors at the storage layer.
* **Schema Normalization:** Converts unstructured security findings into normalized relational rows. This architecture facilitates high-speed cross-referencing and allows for advanced trend analysis (e.g., correlating email patterns across multiple targets) that would be impossible with flat-file storage.

## Problems Solved

* **Intelligence Volatility:** Eliminates the risk of data loss. By transitioning security findings from volatile RAM to disk-backed storage, the system ensures that investigations can be resumed, paused, and audited without data expiry.
* **Standardized Audit Trail:** Generates a deterministic history (`data_scan`) of every operation. This creates an immutable trail of "what was found and when," which is a mandatory requirement for forensic integrity and historical post-incident review.
* **Data Discoverability:** Solves the "data graveyard" problem. By forcing findings into a structured schema, the vault enables the rapid discovery and filtering of specific intelligence, even as the database grows to thousands of entries.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Engine** | `SQLite` | Zero-configuration, serverless, and stores everything in a single portable file—perfect for forensic "carry-on" toolkits. |
| **Security** | Parameterized Queries | The industry standard for preventing SQL Injection; it completely separates the SQL logic from the potentially malicious user data. |
| **Architecture** | Schema Normalization | Reduces data redundancy and ensures that the database remains performant even as we scale from 10 to 10,000+ scan records. |
| **I/O Strategy** | Synchronous Commit | Ensures "Write-Ahead" integrity; if the system crashes during a write, the database rolls back to the last stable state, preventing corruption. |

## Usage

This library serves as the central data storage engine. Ensure the file is saved as `cyber_database.py`.

```python
from cyber_database import CyberVault

# 1. Initialize the storage vault (Creates file if missing)
vault = CyberVault("lab_storage.db")

# 2. Store findings from security reconnaissance
# Normalization is handled internally
vault.save_scan("[https://target.org](https://target.org)", ["sec@target.org", "admin@target.org"])

# 3. Finalize and close the connection safely
vault.close()
