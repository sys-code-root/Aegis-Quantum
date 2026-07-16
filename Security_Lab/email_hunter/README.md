# Web Page Email Extractor

This script searches the text content of a single web page to find and list email addresses. It solves the need to quickly scan an public website layout for contact details without manually reading through the page source code.

## What It Solves

* Collects a target URL from user input and automatically adds the standard secure protocol prefix if it is missing.
* Downloads the public HTML or text content of the specified web page.
* Uses a regular expression string to locate any text matching the standard structure of an email address.
* Filters out duplicate findings automatically to ensure the final listing contains only unique items.
* Prints the resulting list of unique addresses or a failure status note directly to the console.

## Technical Choices

* Written in Python 3 for direct cross-system compatibility and quick scripting setup.
* Uses the third-party requests library to manage the HTTP network connection and pull raw text components.
* Uses the built-in re module to perform fast text pattern matching on the server response body.
* Sets a specific User-Agent configuration header to ensure the network request contains clear context information.
* Implements a 10-second timeout constraint to stop the script from hanging on unresponsive servers.

## Prerequisites

You need Python 3 and the requests library installed on your computer.

Install the required library using pip:

```bash
pip install requests