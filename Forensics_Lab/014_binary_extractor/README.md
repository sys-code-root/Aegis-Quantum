# Binary Extractor & String Utility (Project 014)

A static analysis forensic tool designed to parse binary file structures, establish precise timelines, and mine raw data for human-readable content.

## Technical Explanation

* **MAC Timelines:** Queries OS-level metadata to fetch timestamps (Access, Modification, Creation), crucial for reconstructive session indexing.
* **Header Verification:** Inspects the first 4 bytes of raw binary code (the Magic Numbers) to cross-reference data integrity and alert on extension masking.
* **String Carving:** Employs a specific byte-level regular expression pattern (`rb'[a-zA-Z0-9/._-]{4,}'`) directly on the raw binary stream, capturing plain text indicators of compromise while maximizing processing speed and preserving RAM.

## Problems Solved

* **Malware Code Inspection:** Safely uncovers hidden variables, domains, URLs, or system commands embedded inside compiled programs without detonating them.
* **Masquerading Countermeasures:** Immediately flags malicious payload extensions attempting to pass through security filters as standard images or documents.
* **Temporal Reconstruction:** Builds accurate attack footprints by evaluating exactly when suspicious files arrived and dropped execution tokens onto disk.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Parsing Technique** | Byte-level Regex | Scans raw bytes directly, simulating the native Linux `strings` tool efficiently without loading massive decoded string matrices into RAM. |
| **Fallback Check** | Nested Dict Slice | Properly evaluates short 2-byte structural signals (like `4d5a`) alongside 4-byte blocks without throwing index exceptions. |
| **Memory Isolation** | In-place Decoding | Only decodes the specific text slices isolated by the regex engine, neutralizing character conversion faults during binary streaming. |

## Usage

This tool is optimized for rapid command-line interface (CLI) triage. Run the extractor by passing the target binary path as an argument:

```bash
python binary_extractor.py path/to/artifact.bin
