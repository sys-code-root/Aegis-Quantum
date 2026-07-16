# Cyber Archive Data Exporter

This script extracts security target scan logs from a local SQLite database to export text reports and save binary data backups. It solves the need to move database entries into readable spreadsheet files and archive database states for recovery purposes.

## What It Solves

* Connects to a local SQLite database file to pull records directly from the targets table.
* Parses database rows into a structured CSV text file with defined column headers for ID, URL, Emails, and Scan Date.
* Serializes the extracted row data into a single binary backup file to preserve the exact raw data layout.
* Includes exception handling blocks to catch database extraction failures and closes data connections safely to avoid file locks.

## Technical Choices

* Written in Python 3 to ensure direct script execution across different operating systems.
* Uses the native sqlite3 module to manage database read connections and process SQL queries.
* Uses the built-in csv library to handle text formatting, row splitting, and UTF-8 encoding variables during file writes.
* Uses the standard pickle module to handle raw object serialization into binary dump files.

## Prerequisites

* Python 3 installed on your local system.
* A local SQLite database file named `cyber_security.db` containing a `targets` table filled with compatible log information.
* No third-party pip installations are required because the script relies entirely on standard built-in Python modules.

## How to Run

Save the script as `cyber_archive.py` and run it from your command line terminal:

```bash
python cyber_archive.py