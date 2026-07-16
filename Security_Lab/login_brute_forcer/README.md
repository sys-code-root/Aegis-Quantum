# Login Credential Tester

This script tests authentication security by submitting a list of passwords for a specific username against a target login URL. It solves the need to check whether user accounts are vulnerable to dictionary lookups or weak passwords found in common lists.

## What It Solves

* Automates the submission of login forms by sending HTTP POST requests with credential payloads.
* Reads a local text file containing candidate passwords line by line, stripping out whitespace.
* Checks the text body of the web response for a specific error indicator ("Invalid") to determine if authentication failed.
* Captures and logs successful credential matches when the failure indicator is missing from the response.
* Controls connection stability by using a 5-second timeout on network tasks to avoid process freezes.

## Technical Choices

* Written in Python 3 for quick setup and execution inside command line shells.
* Uses the third-party requests library to manage web requests, post form data, and read server responses.
* Employs standard sequential text file streaming to ensure low memory use when reading long wordlists.
* Uses built-in try-except blocks to catch connection dropouts and missing wordlist errors without crashing the script.

## Prerequisites

You need Python 3 and the requests library installed on your computer. You also need a plain text file containing candidate passwords.

Install the required library using pip:

```bash
pip install requests