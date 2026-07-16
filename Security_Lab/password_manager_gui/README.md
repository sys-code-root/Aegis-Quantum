# Secure Password Generator and Database Archivist

This script builds a graphical user interface window to generate random, high-entropy passwords based on a user-defined length and automatically archive them to a local database. It solves the need for generating secure passwords and storing them alongside their target services safely inside a local file database without manual logging.

## What It Solves

* Spawns a dedicated dark-themed window interface to manage credential generation tasks.
* Generates a random string using character blocks that mix uppercase letters, lowercase letters, numerical digits, and special symbols.
* Validates user input field parameters to ensure password length is configured as a numeric integer and that the target service name field is not left blank.
* Connects to a local SQLite database file named `cyber_security.db` and sets up the internal target registry table if missing.
* Persists records safely by saving the service name to the `url` column and the formatted password string directly to the `emails` column inside the `targets` table.
* Displays responsive dialog warnings for data parsing exceptions and success alerts for data archiving updates.

## Technical Choices

* Written in Python 3 for immediate portability across multiple desktop systems.
* Uses the native `tkinter` module to render layout forms, label descriptions, data entries, and graphical grids.
* Uses the built-in `messagebox` library to trigger asynchronous system notifications for validation and processing updates.
* Uses the native `sqlite3` library to write and read data directly into a single file system asset, avoiding the need to run an external database engine server.
* Uses the standard `random` and `string` modules to pick character variations securely and stitch them together into custom lengths.

## Prerequisites

* Python 3 installed on your local computer.
* This tool relies completely on native Python standard libraries, so there is no need for external pip installations or third-party package dependencies.

## How to Run

Save the script code as `password_manager.py` and run it from your command terminal:

```bash
python password_manager.py