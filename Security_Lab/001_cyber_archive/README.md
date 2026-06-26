# Cyber Report & Archive Tool (Project 025)

A high-assurance data management utility designed to handle the persistence lifecycle of forensic intelligence. This tool facilitates the transition from raw database storage to interoperable reporting formats and redundant binary archival, ensuring audit integrity and disaster recovery resilience.

## Technical Explanation

* **Relational-to-Flat Serialization:** Transforms structured SQL records into CSV (Comma-Separated Values) structures. This ensures human-readable reporting and interoperability with standard spreadsheet processors, critical for client-side audit delivery.
* **Complex Object Persistence:** Implements Python's `pickle` library for binary object serialization. Unlike SQL or CSV, this preserves the exact state of Python objects (including nested structures), allowing for exact state restoration of security targets, effectively decoupling data from the primary database engine.
* **Redundancy & Disaster Recovery:** Manages the backup lifecycle by maintaining dual-format archival. This mitigates the risk of data loss during system wipes, directory rotations, or primary database file corruption, providing a fail-safe recovery mechanism for collected intelligence.

## Problems Solved

* **Reporting Latency:** Automates the extraction of scanner data into formatted reports. This eliminates manual data manipulation, reducing the "Time to Report" for security audits and penetration testing debriefs.
* **Offline Data Recovery:** Solves the critical issue of primary database failure. By maintaining a `.pkl` state file, the system can reconstruct the scanner's full memory/data state even if the SQL primary database file suffers structural corruption.
* **Data Portability:** Facilitates the sharing of forensic artifacts with non-technical stakeholders (auditors, management) via standardized CSV formatting, while keeping a "system-ready" binary version for technical forensics.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Reporting Format** | CSV | Standard industry format for audit logs. It is universally compatible with Excel, SIEMs, and other data analysis tools. |
| **Archival Format** | Pickle | Unlike text formats, Pickle handles complex Python objects natively. It is the fastest way to save/restore the exact application state. |
| **Redundancy** | Dual-Format Storage | We separate "Reporting" (CSV) from "Recovery" (Pickle). One is for the client, the other is for the system's own forensic continuity. |
| **Architecture** | decoupled I/O | The tool does not store files in the DB path directly; it exports them, ensuring the integrity of the archival is never impacted by the primary DB's activity. |

## Usage

This utility is designed to be the final step in your data persistence pipeline. Ensure the file is saved as `cyber_archive.py`.

```python
from cyber_archive import CyberArchive

# 1. Initialize the archival system using your primary storage file
vault = CyberArchive("security_vault.db")

# 2. Run the full data persistence lifecycle
# Export to CSV for audit reports
vault.export_to_csv("monthly_audit.csv")

# Create a binary system backup for disaster recovery
vault.backup_objects_pickle("monthly_backup.pkl")
