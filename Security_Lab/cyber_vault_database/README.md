# Target Log Database Vault

This script sets up a local SQLite database to store and organize extracted web address details and email lists. It solves the need to persist information gathered during network scans, ensuring data is saved with automated timestamps for future review instead of being lost when the terminal closes.

## What It Solves

* Automatically creates a database file named `cyber_security.db` upon initial execution.
* Checks for and initializes the internal data layout using a table named `targets`.
* Converts Python list objects into comma-separated text strings for clean cell storage.
* Generates custom system timestamps to track exactly when each entry is written to the disk.
* Uses parameterized SQL operations to handle data injection boundaries safely.

## Technical Choices

* Written in Python 3 for immediate cross-system command line execution.
* Uses the built-in sqlite3 library to keep data management lightweight and independent of standalone database engine servers.
* Uses the native datetime module to handle runtime formatting patterns for the log parameters.
* Organizes database connection management inside structural class calls to separate initialization steps from runtime inserts.

## Prerequisites

* Python 3 installed on your local computer.
* No external libraries or pip installation commands are required as this tool uses standard Python components.

## How to Run

Save the script code as `database_vault.py` and run it from your command terminal:

```bash
python database_vault.py