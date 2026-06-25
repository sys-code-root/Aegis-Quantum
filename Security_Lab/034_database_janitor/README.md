# Database Janitor (Project 034)

An architectural management and maintenance suite designed for the Security Vault. This utility ensures database hygiene by managing data lifecycles, enabling precise updates, and enforcing rigorous record deletion protocols to maintain the accuracy of stored intelligence.

## Technical Explanation

* **Atomic Transaction Management:** Implements mandatory `.commit()` protocols for all mutation operations. This ensures that changes are only persisted if the transaction is completed successfully, upholding ACID (Atomicity, Consistency, Isolation, Durability) principles within the forensic database.
* **Operational Feedback Loop:** Utilizes SQL `rowcount` validation to confirm mutations. This prevents "silent failures" where a script might report success despite zero rows being modified, ensuring the analyst has 100% visibility into the state of the data.
* **Data Sanitization Logic:** Provides controlled entry points for CRUD (Create, Read, Update, Delete) operations, ensuring that the database remains a "clean room" for OSINT artifacts rather than a collection of stale or misleading intelligence.

## Problems Solved

* **Data Pollution & False Positives:** Prevents the accumulation of "stale" or irrelevant intelligence artifacts. By removing outdated records, the janitor ensures that subsequent OSINT analysis is performed on accurate, high-fidelity datasets.
* **Forensic Lifecycle Compliance:** Supports data governance and privacy standards. In forensic engagements, it is often necessary to purge specific records based on scope limitations; this tool provides the programmatic path to do so.
* **Operational Accuracy:** Eliminates the risk of logic errors stemming from legacy data. By maintaining a strict hygiene policy, the database remains a reliable "source of truth" for the investigation.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Transactionality** | `.commit()` | Ensures that if an update/delete fails halfway, the database rolls back to its last known-good state, preventing corruption. |
| **Integrity** | `rowcount` Validation | Forensic tools must never fail silently. Checking affected row counts provides immediate verification that the intended operation was executed. |
| **Safety** | Targeted Mutation | By isolating update/delete logic into specific methods, we prevent the "oops" scenario of wiping the entire database via a malformed query. |
| **Persistence** | Serverless SQLite | Keeps the "Vault" portable. The janitor works directly on the file, meaning it can be deployed on a clean forensic machine without needing to configure a DB server. |

## Usage

This utility is designed to be the administrative backbone of your database operations. Ensure the file is saved as `database_janitor.py`.

```python
from database_janitor import DatabaseJanitor

# Instantiate janitorial control for the forensic vault
janitor = DatabaseJanitor("lab_storage.db")

# 1. Rectify metadata for a target record (Update)
janitor.update_email(5, "new_contact@target.com")

# 2. Purge obsolete or sensitive records (Delete)
janitor.delete_record(12)

# 3. Finalize and close the connection
janitor.close()
