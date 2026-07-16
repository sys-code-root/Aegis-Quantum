# Web Directory Finder

This script checks for the presence of directories and files on a web server by appending words from a text list to a target URL. It solves the need to verify which common paths are accessible or restricted on a web server during routine configuration audits.

## What It Solves

* Automatically appends a trailing slash to the target URL if missing to ensure correct path construction.
* Reads an input wordlist file line by line while skipping empty lines and comments that start with a hash symbol.
* Sends HTTP GET requests to each combined URL link to verify its current live status.
* Displays explicit notifications for accessible folders using 200 OK responses and restricted folders using 403 Forbidden responses.
* Drops dead or slow connections cleanly using a built-in timeout limit to prevent the program from freezing.

## Technical Choices

* Written in Python 3 for quick script modification and cross-system execution.
* Uses the third-party requests library to manage network connections, send headers, and read HTTP response status codes.
* Defines a specific User-Agent header string to keep network connection contexts clear.
* Implements a 3-second timeout limit on individual network operations to handle lagging servers efficiently.

## Prerequisites

You need Python 3 and the requests library installed on your computer. You also need a local text file containing directory names to test.

Install the required library using pip:

```bash
pip install requests