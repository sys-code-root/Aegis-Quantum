# Forensic File Hasher (Project 022)

A cryptographic integrity utility designed to generate immutable digital fingerprints (SHA-256) for forensic artifacts, essential for maintaining secure chain-of-custody records.

## Technical Explanation

* **Collision-Resistant Fingerprinting:** Implements the SHA-256 algorithm to create a unique signature, ensuring that even single-bit modifications are detected during re-verification.
* **Buffered Binary Streaming:** Processes target files using `4KB` chunk streams, ensuring system-level performance remains fluid even when hashing massive forensic drive images (e.g., `.E01` or `.dd` files).
* **Exception-Driven Error Architecture:** Rejects type-polluted string error returns by raising strict, native `FileNotFoundError` exceptions when handling missing artifacts, guaranteeing predictable and deterministic tracking behavior during pipeline automation.

## Problems Solved

* **Chain of Custody Verification:** Allows investigators to prove mathematically that an evidence file currently under analysis is completely identical to the file captured at the physical or virtual crime scene.
* **Metadata Forgery Detection:** Effectively exposes "timestomping" or hidden payload injections, as any alteration to the underlying binary matrix results in an immediate and total hash mismatch.
* **Data Integrity Assurance:** Validates that network data transfer, ingestion, or storage-to-storage copying operations during collection did not result in structural corruption or bit-rot.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Algorithm** | SHA-256 | Offers superior collision resistance compared to outdated legacy protocols like MD5 or SHA-1, fully aligning with modern judicial and industrial standards. |
| **IO Strategy** | 4KB Buffer Blocks | Prevents the operating system from loading massive binary blocks into memory, keeping RAM utilization flat and eliminating the risk of heap overflows. |
| **Encoding** | `rb` (Read Binary) | Crucial for forensic integrity; forces raw byte stream processing regardless of local text-encoding tables or complex file headers. |
| **Error Model** | Native Exceptions | Raising explicit exceptions rather than returning error strings separates tracking telemetry metrics from execution fault paths. |

## Usage

This tool is optimized for command-line interface (CLI) execution. Pass the target artifact path directly as an argument to calculate its signature:

```bash
python file_hasher.py path/to/evidence.dd
