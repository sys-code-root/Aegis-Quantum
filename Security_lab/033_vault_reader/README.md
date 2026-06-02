# Vault Intelligence Reader (Project 033)

A data retrieval interface that allows security operators to query,
filter, and review stored intelligence artifacts within the Security
Lab\'s vault.

## Technical Explanation

-   **Chronological Indexing:** Employs *ORDER BY id DESC* to prioritize
    the most recent security observations for immediate triage.
-   **Partial Match Querying:** Leverages SQL *LIKE* operators with
    wildcard patterns (*%*) to enable flexible search functionality
    across stored URL targets.
-   **Injection-Proof Retrieval:** Continues the use of parameterized
    SQL queries to ensure that even search inputs are handled safely by
    the database engine.

## Problems Solved

1.  **Intelligence Searchability:** Transforms a static database file
    into a searchable repository of past scans and OSINT findings.
2.  **Contextual Retrieval:** Allows investigators to quickly pull up
    previous intelligence artifacts related to specific domains or IPs
    during live investigations.

## Usage

from 033_vault_reader import VaultReader\
\
\# Connect to the intelligence vault\
reader = VaultReader(\"lab_storage.db\")\
\
\# Review historical intelligence logs\
reader.list_all_scans()\
\
\# Query artifacts related to a specific target domain\
reader.search_by_url(\"google.com\")
