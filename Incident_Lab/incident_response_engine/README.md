# Incident Response Engine

This script automates file triage and cleanup tasks inside a target directory. It solves the need to recursively find and delete risky file extensions, strip potentially tracking metadata from images, and extract hidden web links embedded in PDF documents.

## What It Solves

* Deletes suspicious files containing extensions like .exe, .bat, or .scr, or words like virus and malware in their filenames.
* Sanitizes image files (.jpg, .jpeg, .png) by copying the raw image data into a brand new file container, which effectively strips away all original metadata.
* Inspects PDF documents to parse page annotations and log any embedded web links (URIs) found inside them.
* Automatically writes all alerts, errors, and actions with timestamps to a local log file.

## Technical Choices

* Written in Python 3 using a mix of standard modules and specific parsing libraries.
* Uses the pathlib module to handle recursive file searching seamlessly across different operating systems.
* Uses the re module to run case-insensitive filename matching against a precompiled pattern.
* Uses the Pillow library to safely rebuild image files to clear old metadata.
* Uses the pdfplumber library to open PDF layers and check for underlying URL links.

## Prerequisites

You need Python 3 installed along with the pdfplumber and Pillow libraries.

Install the required packages using pip:

```bash
pip install pdfplumber Pillow