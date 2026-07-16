# Image EXIF Analyser

This script extracts EXIF metadata and GPS location details from image files. It solves the need to quickly view hidden data embedded in photos, such as camera models, dates, and coordinates, using the command line.

## Technical Choices

* Written in Python 3 for simplicity and cross-platform compatibility.
* Uses the Pillow library to read image metadata without loading the full image into memory unnecessarily.
* Uses built-in Python modules (os, sys) to check file existence and handle command-line arguments.
* Includes text decoding handling to prevent script crashes when encountering raw byte segments in the metadata.

## Prerequisites

You need Python 3 and the Pillow library installed on your system.

Install the required library using pip:

```bash
pip install Pillow