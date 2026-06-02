# Binary Extractor & String Utility (Project 014)

A static analysis forensic tool designed to parse binary file
structures, establish precise timelines, and mine raw data for
human-readable content.

## Technical Explanation

-   **MAC Timelines:** Queries OS-level metadata to fetch timestamps
    (Access, Modification, Creation), crucial for reconstructive session
    indexing.
-   **Header Verification:** Inspects the first 4 bytes of raw binary
    code (the Magic Numbers) to cross-reference data integrity and alert
    on extension masking.
-   **String Carving:** Employs a specific regular expression pattern
    (*\[a-zA-Z0-9/.\_-\]{4,}*) combined with an alternative encoding
    error override to drop non-printable machine instructions while
    leaving plain text intact.

## Problems Solved

1.  **Malware Code Inspection:** Safely uncovers hidden variables,
    domains, URLs, or system commands embedded inside compiled programs
    without detonating them.
2.  **Masquerading Countermeasures:** Immediately flags malicious
    payload extensions attempting to pass through security filters as
    standard images or documents.
3.  **Temporal Reconstruction:** Builds accurate attack footprints by
    evaluating exactly when suspicious files arrived and dropped
    execution tokens onto disk.

## Design Decisions: \"Why this instead of that?\"

  ----------------------- --------------------- --------------------------------------------------------------------------------------------------------------------------------
  **Parsing Technique**   Regex Scan            Simulates the traditional Linux *strings* tool natively within Python, eliminating cross-platform subshell compilation issues.
  **Error Flagging**      *errors=\'ignore\'*   Prevents character conversion faults from crashing stack routines when streaming wide UTF block matrices.
  **Fallback Check**      Nested dict slice     Properly evaluates short 2-byte structural signals (like *4d5a*) without throwing index exceptions.
  ----------------------- --------------------- --------------------------------------------------------------------------------------------------------------------------------

## Usage

from 014_binary_extractor import BinaryExtractor\
\
extractor = BinaryExtractor(\"malicious_artifact.bin\")\
extractor.get_file_stats()\
extractor.verify_header()\
extractor.extract_strings()
