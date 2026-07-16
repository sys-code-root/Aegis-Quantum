# Forensic File Hasher

This project is a command-line script that computes the SHA-256 hash of a file. It is used in digital forensics and file analysis to verify integrity and ensure that a target file has not been altered or tampered with.

## Technical Choices

* Python Standard Libraries: The script relies entirely on built-in modules (hashlib, os, sys), meaning it requires zero external dependencies or package installations.
* SHA-256 Algorithm: Chosen for reliable and cryptographically secure file integrity verification.
* Buffered Reading: The script reads files in blocks of 4096 bytes. This prevents memory issues when hashing very large files, as it keeps memory usage low and stable.

## Requirements

* Python 3.x

## How to Use

Save the script as file_hasher.py and run it from your terminal by passing the path of the file you want to analyze as an argument.

Command syntax:
python file_hasher.py <path_to_artifact>

Example command:
python file_hasher.py evidence.bin

## Expected Output

When execution is successful, the script will display the calculated hash:

==================================================
      FORENSIC FILE HASHER (SHA-256)
==================================================

[*] Computing cryptographic DNA fingerprint...
[+] Integrity Signature (SHA-256): e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
==================================================

If the file does not exist, the script catches the error and reports that the target artifact was not found.