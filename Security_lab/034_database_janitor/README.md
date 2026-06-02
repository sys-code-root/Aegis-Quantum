# Database Janitor (Project 034)

An administrative utility for the Security Vault, enabling the update
and deletion of stored intelligence records to maintain database hygiene
and accuracy.

## Technical Explanation

-   **Data Sanitization:** Implements SQL *UPDATE* and *DELETE*
    operations to correct intelligence artifacts that were harvested
    incorrectly or are no longer relevant.
-   **Rowcount Validation:** Uses SQL operational feedback (*rowcount*)
    to provide immediate confirmation of successful data mutations,
    preventing \"silent failures.\"
-   **Atomic Transactions:** Utilizes *.commit()* to ensure data
    consistency during modifications.

## Problems Solved

1.  **Database Corruption/Inaccuracy:** Prevents the accumulation of
    \"stale\" intelligence that could lead to false positives during
    OSINT analysis.
2.  **Storage Management:** Allows for the removal of sensitive or
    unwanted records, supporting data privacy and lifecycle compliance.

## Usage

from 034_database_janitor import DatabaseJanitor\
\
\# Instantiate janitorial control\
janitor = DatabaseJanitor(\"lab_storage.db\")\
\
\# Rectify metadata for a target record\
janitor.update_email(5, \"new_contact@target.com\")\
\
\# Purge obsolete or sensitive records\
janitor.delete_record(12)\
\
janitor.close()
