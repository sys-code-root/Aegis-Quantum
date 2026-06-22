# Cyber Report & Archive Tool (Project 025)

An operational data management utility designed to handle the
persistence lifecycle of database entries, allowing for portable
reporting (CSV) and raw data archival (Pickle).

## Technical Explanation

-   **Data Serialization:** Transforms relational database records into
    CSV structures for human-readable reporting and spreadsheet
    integration.
-   **Object Persistence:** Uses Python's *pickle* library to serialize
    complex data lists into binary blobs, allowing for exact state
    restoration of security targets without needing a SQL engine
    present.
-   **Redundancy Management:** Ensures that all intelligence collected
    throughout operational cycles is backed up, preventing accidental
    data loss during system wipes or directory rotations.

## Problems Solved

1.  **Reporting Latency:** Automates the extraction of scanner data into
    spreadsheets, significantly reducing the time spent generating audit
    reports.
2.  **Offline Data Recovery:** Provides a secondary recovery mechanism
    (*.pkl*) to reconstruct the scan database even if the SQL primary
    database file suffers corruption.

## Usage

from cyber_archive.py import CyberArchive\
\
\# Initialize archival system\
vault = CyberArchive(\"security_vault.db\")\
\
\# Run full monthly data persistence lifecycle\
vault.export_to_csv(\"monthly_audit.csv\")\
vault.backup_objects_pickle(\"monthly_backup.pkl\")
