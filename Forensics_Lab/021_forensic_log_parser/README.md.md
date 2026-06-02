# Forensic Log Parser & Incident Auditor (Project 021)

A post-incident log forensics engine designed to parse massive system
text logs line-by-line, isolating indicators of compromise (IoCs),
privilege escalation attempts, and auth mechanisms.

## Technical Explanation

-   **Streaming Log Extraction:** Uses memory-safe line-by-line
    iterations over file descriptors, allowing the parser to process
    multi-gigabyte log dumps without causing RAM exhaustion.
-   **Character Encoding Shielding:** Implements explicit alternative
    error handling (*errors=\'ignore\'*) to prevent application crashes
    when dealing with broken bytes or binary structures hidden within
    text lines.
-   **Algorithmic Signature Matching:** Converts lines to uniform
    uppercase matrices dynamically to perform high-speed string
    intersections against explicit evaluation definitions.

## Problems Solved

1.  **Brute-Force Attack Discovery:** Instantly filters out thousands of
    noise lines to group systemic failure events (*AUTH_FAILURE*,
    *DENIED*, *INVALID*).
2.  **Unauthorized Elevation Detection:** Flags unauthorized usage of
    high-privilege scopes (*SUDO*, *ROOT*) to audit insider threats or
    account takeovers.
3.  **Massive Data Trailing Noise Reduction:** Saves investigators hours
    of manual searching by condensing massive raw text dumps into a
    clean list of high-risk operational events.

## Design Decisions: \"Why this instead of that?\"

  ---------------------- ------------------------------ -------------------------------------------------------------------------------------------------------------------------------
  **I/O Pattern**        Line-by-Line Generator         Far superior to *.readlines()*, which dumps the entire file into RAM and crashes when opening real enterprise log structures.
  **Parsing Strategy**   Standard String Intersection   High-speed keyword filtering matches flat system signatures faster than heavy regular expression loops.
  **Data Enforcement**   Encoding Failure Drops         Drops corrupted formatting blocks natively, keeping the structural timeline integrity solid without interruptions.
  ---------------------- ------------------------------ -------------------------------------------------------------------------------------------------------------------------------

## Usage

from 021_forensic_log_parser import ForensicLogParser\
\
\# Instantiate the parser over an unverified system log dump\
parser = ForensicLogParser(\"/var/log/auth.log\")\
\
\# Run the forensic triage sweep\
parser.parse_logs()
