# Database Log Modifier

This script modifies or removes specific scan logs stored inside a local SQLite database. It solves the need to fix incorrect email entries or permanently delete old target records by their identifier numbers using a command-line interface.

## What It Solves

* Establishes a direct connection to a local SQLite database file to manage storage entries.
* Updates the email data string for a targeted record using its unique row ID number.
* Deletes an entire log entry from the database table based on user input.
* Includes validation checks using row counts to notify you if the target ID exists or missing from the table.
* Adds a text-based confirmation step to avoid accidental deletions of storage logs.

## Technical Choices

* Written in Python 3 for direct execution across standard command terminal shells.
* Uses the native sqlite3 module to manage text rows without needing a separate database server setup.
* Uses parameterized queries with question mark placeholders to pass data safely into the database engine.
* Employs standard conditional blocks to catch incorrect ID entries and manage script flow.

## Prerequisites

* Python 3 installed on your machine.
* A local SQLite database file named `cyber_security.db` in the same directory, containing a `targets` table with `id` and `emails` columns.
* No external third-party libraries or installation commands are required.

## How to Run

Save the script code as `db_janitor.py` and run it from your command line:

```bash
python db_janitor.py