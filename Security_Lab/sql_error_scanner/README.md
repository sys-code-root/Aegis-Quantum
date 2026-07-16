# SQL Error Scanner

This script checks how a web application handles database input errors by appending a single quote to a URL query parameter. It solves the need to verify if a web application exposes raw database error strings to users, which can reveal underlying security weaknesses.

## What It Solves

* Collects a target URL containing a query parameter directly from terminal input.
* Modifies the URL path by appending a single quote character to provoke a database response layout change.
* Sends an HTTP GET request to the modified link while preventing automatic URL redirects.
* Scans the returned response text against a predefined list of database error signatures from engines like MySQL, PostgreSQL, Oracle, and SQLite.
* Prints clear status indicators explaining if a database error string was discovered or if the check came back clean.

## Technical Choices

* Written in Python 3 to ensure cross-system execution without complex setup routines.
* Uses the third-party requests library to build HTTP network tasks and read server body text simply.
* Fixes a 5-second timeout limit to stop the terminal process from freezing on non-responsive endpoints.
* Disables the redirect tracking behavior to look exclusively at the immediate raw server response text.

## Prerequisites

You need Python 3 and the requests library installed on your system.

Install the required library using pip:

```bash
pip install requests