# Database Vault Reader

This script reads and searches log entries stored inside a local SQLite database. It solves the need to view previously saved scan summaries, list historical entries in order, and look up specific target web addresses using keywords.

## What It Solves

* Establishes a read connection to an existing SQLite database file named `cyber_security.db`.
* Displays a complete list of historical logs sorted by ID in descending order.
* Implements a search function that filters the database using partial text matches on the URL column.
* Prints stored data objects, including the ID numbers, target names, capture timestamps, and extracted email lists, straight to the terminal window.
* Closes database connections cleanly at the end of the script execution loop to maintain file integrity.

## Technical Choices

* Written in Python 3 for direct cross-system execution from the command line.
* Uses the native sqlite3 library to interact with database files without setting up local database server engines.
* Employs standard parameterized SQL queries (`LIKE ?`) to handle wildcard text search inputs safely.
* Structures database actions inside an object-oriented layout to keep connections and resource cleanups organized.

## Prerequisites

* Python 3 installed on your machine.
* A local SQLite database file named `cyber_security.db` present in the same folder, containing a `targets` table with `id`, `url`, `emails`, and `data_scan` columns.
* No external third-party pip packages are required because the script uses built-in Python tools.

## How to Run

Save the script file as `vault_reader.py` and execute it from your terminal session:

```bash
python vault_reader.py