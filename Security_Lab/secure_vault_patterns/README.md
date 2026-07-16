# Database Query Security Demonstrator

This script demonstrates the operational difference between insecure and secure database search queries. It solves the need to understand and fix SQL injection vulnerabilities by comparing direct string formatting against parameterized input methods when interacting with a local database table.

## What It Solves

* Establishes a direct connection to a local SQLite tracking database file.
* Demonstrates how raw f-string variable interpolation inside SQL strings causes security vulnerabilities by failing to escape user characters.
* Demonstrates how to block input manipulation tactics by passing user arguments through a dedicated parameters tuple.
* Safely retrieves target record datasets matching a specific web address without risk of backend query altering.

## Technical Choices

* Written in Python 3 for clean, lightweight terminal execution and simple scripting.
* Uses the built-in sqlite3 database module to manage local storage without deploying external database engine systems.
* Implements the standard question mark placeholder syntax to sanitize input variables inside the database driver.
* Wraps database connection objects and cursor variables inside a clean class block to keep the code modular.

## Prerequisites

* Python 3 installed on your machine.
* A local SQLite database file named `cyber_security.db` containing a `targets` table with a populated `url` column.
* No third-party pip packages are required because the program runs entirely on the Python standard library.

## How to Run

To test this class layout, save the code as `secure_patterns.py`. You can append an entry point block to instantiate the object, or import the module into a separate runner script.

Execute the script from your terminal:

```bash
python secure_patterns.py