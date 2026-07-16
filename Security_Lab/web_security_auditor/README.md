# HTTP Security Header Auditor

This script audits a web application's configuration by checking its HTTP response headers and cookie security flags. It solves the need to quickly verify if important defense headers and session flags are missing from a target web server.

## What It Solves

* Collects a target URL from user input and ensures it includes the correct web protocol prefix.
* Inspects the server response for four standard configuration headers: X-Frame-Options, X-Content-Type-Options, Content-Security-Policy, and Strict-Transport-Security.
* Logs whether each header is present or missing to evaluate the basic configuration status.
* Checks any returned cookies to confirm whether the HttpOnly flag is enabled, which helps protect session identifiers.

## Technical Choices

* Written in Python 3 for clean terminal deployment and testing.
* Uses the third-party requests library to handle connection variables and inspect network response objects.
* Employs an HTTP HEAD request rather than a GET request to read header names quickly without downloading the web page body text.
* Enforces a 5-second connection timeout to keep the script from hanging on non-responsive target addresses.
* Uses internal string matching logic to safely parse non-standard cookie structural parameters.

## Prerequisites

You need Python 3 and the requests package installed on your local computer.

Install the required library using pip:

```bash
pip install requests